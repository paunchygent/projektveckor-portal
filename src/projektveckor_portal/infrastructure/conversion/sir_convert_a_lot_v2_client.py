from __future__ import annotations

import json
from dataclasses import dataclass
from typing import IO
from uuid import uuid4

import httpx
from pydantic import BaseModel, ConfigDict, Field

from projektveckor_portal.interfaces.conversion import (
    ConversionClient,
    ConversionJobRecord,
    ConversionJobSpec,
)

_TERMINAL_FAILURE_STATUSES = {"failed", "canceled", "cancelled"}


class _JobPayload(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True, str_strip_whitespace=True)

    job_id: str = Field(min_length=1)
    status: str = Field(min_length=1)


class _CreateJobResponsePayload(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    job: _JobPayload


@dataclass(frozen=True, slots=True)
class SirConvertALotConfig:
    base_url: str
    api_key: str


class SirConvertALotV2Client(ConversionClient):
    """HTTP adapter for Sir Convert a Lot v2 job submission/polling.

    Notes:
    - Portal uses deterministic idempotency keys for create-job.
    - If the server replies with `X-Idempotent-Replay: true` and the replayed job is
      terminal failed/canceled, we submit once more with a fresh idempotency key.
      This matches the UX expectation that "rerun after fix" should be simple.
    """

    def __init__(
        self, *, config: SirConvertALotConfig, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        self._config = config
        self._transport = transport

    async def create_job(self, *, spec: ConversionJobSpec, content: bytes) -> ConversionJobRecord:
        base_idempotency_key = self._idempotency_key(spec=spec, content=content)
        return await self._create_job_with_idempotency_key(
            spec=spec,
            content=content,
            idempotency_key=base_idempotency_key,
            allow_auto_rerun=True,
        )

    async def _create_job_with_idempotency_key(
        self,
        *,
        spec: ConversionJobSpec,
        content: bytes,
        idempotency_key: str,
        allow_auto_rerun: bool,
    ) -> ConversionJobRecord:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs"
        headers = {"X-API-Key": self._config.api_key, "Idempotency-Key": idempotency_key}

        job_spec = {
            "api_version": "v2",
            "source": {
                "kind": "upload",
                "filename": spec.source_filename,
                "format": spec.source_format,
            },
            "conversion": {
                "output_format": spec.output_format,
                "css_filenames": [],
                "reference_docx_filename": None,
            },
            "retention": {"pin": False},
        }
        FileValue = (
            IO[bytes]
            | bytes
            | str
            | tuple[str | None, IO[bytes] | bytes | str]
            | tuple[str | None, IO[bytes] | bytes | str, str | None]
        )
        files: list[tuple[str, FileValue]] = [
            ("file", (spec.source_filename, content, "application/octet-stream")),
            ("job_spec", (None, json.dumps(job_spec), "application/json")),
        ]

        async with httpx.AsyncClient(timeout=30.0, transport=self._transport) as client:
            response = await client.post(url, headers=headers, files=files)
            response.raise_for_status()
            payload = _CreateJobResponsePayload.model_validate(response.json())
            is_idempotent_replay = response.headers.get("X-Idempotent-Replay", "").lower() == "true"

        normalized_status = payload.job.status.strip().lower()
        if (
            allow_auto_rerun
            and is_idempotent_replay
            and normalized_status in _TERMINAL_FAILURE_STATUSES
        ):
            # Retry UX: a failed replay is not useful after a fix. Submit once with a fresh
            # idempotency key so downstream doesn't need to "change filename" to rerun.
            rerun_idempotency_key = f"{idempotency_key}_rerun_{uuid4().hex}"
            return await self._create_job_with_idempotency_key(
                spec=spec,
                content=content,
                idempotency_key=rerun_idempotency_key,
                allow_auto_rerun=False,
            )

        return ConversionJobRecord(job_id=payload.job.job_id, status=payload.job.status)

    async def get_job(self, *, job_id: str) -> ConversionJobRecord:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs/{job_id}"
        headers = {"X-API-Key": self._config.api_key}
        async with httpx.AsyncClient(timeout=8.0, transport=self._transport) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            payload = _CreateJobResponsePayload.model_validate(response.json())
        return ConversionJobRecord(job_id=payload.job.job_id, status=payload.job.status)

    async def download_artifact(self, *, job_id: str) -> bytes:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs/{job_id}/artifact"
        headers = {"X-API-Key": self._config.api_key}
        async with httpx.AsyncClient(timeout=30.0, transport=self._transport) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.content

    def _idempotency_key(self, *, spec: ConversionJobSpec, content: bytes) -> str:
        import hashlib

        h = hashlib.sha256()
        h.update(spec.source_filename.encode("utf-8"))
        h.update(spec.source_format.encode("utf-8"))
        h.update(spec.output_format.encode("utf-8"))
        h.update(hashlib.sha256(content).digest())
        return f"idem_pvp_{h.hexdigest()[:48]}"
