from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx

from projektveckor_portal.interfaces.conversion import (
    ConversionClient,
    ConversionJobRecord,
    ConversionJobSpec,
)


@dataclass(frozen=True, slots=True)
class SirConvertALotConfig:
    base_url: str
    api_key: str


class SirConvertALotV2Client(ConversionClient):
    def __init__(self, *, config: SirConvertALotConfig) -> None:
        self._config = config

    async def create_job(self, *, spec: ConversionJobSpec, content: bytes) -> ConversionJobRecord:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs"
        headers = {
            "X-API-Key": self._config.api_key,
            "Idempotency-Key": self._idempotency_key(spec=spec, content=content),
        }
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
            "execution": {"priority": "normal", "document_timeout_seconds": 1800},
            "retention": {"pin": False},
        }
        files: list[tuple[str, Any]] = [
            ("file", (spec.source_filename, content, "application/octet-stream")),
            ("job_spec", (None, json.dumps(job_spec), "application/json")),
        ]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, files=files)
            response.raise_for_status()
            payload = response.json()

        job_id = str(payload.get("job_id", "")).strip()
        status = str(payload.get("status", "")).strip()
        return ConversionJobRecord(job_id=job_id, status=status)

    async def get_job(self, *, job_id: str) -> ConversionJobRecord:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs/{job_id}"
        headers = {"X-API-Key": self._config.api_key}
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            payload = response.json()
        status = str(payload.get("status", "")).strip()
        return ConversionJobRecord(job_id=job_id, status=status)

    async def download_artifact(self, *, job_id: str) -> bytes:
        url = f"{self._config.base_url.rstrip('/')}/v2/convert/jobs/{job_id}/artifact"
        headers = {"X-API-Key": self._config.api_key}
        async with httpx.AsyncClient(timeout=30.0) as client:
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
