from __future__ import annotations

import asyncio

import httpx

from projektveckor_portal.infrastructure.conversion.sir_convert_a_lot_v2_client import (
    SirConvertALotConfig,
    SirConvertALotV2Client,
)
from projektveckor_portal.interfaces.conversion import ConversionJobSpec


def test_create_job_auto_reruns_failed_idempotent_replay() -> None:
    seen_idempotency_keys: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        idempotency_key = request.headers.get("Idempotency-Key")
        assert idempotency_key is not None
        seen_idempotency_keys.append(idempotency_key)

        if len(seen_idempotency_keys) == 1:
            return httpx.Response(
                200,
                headers={"X-Idempotent-Replay": "true"},
                json={"job": {"job_id": "job_old", "status": "failed"}},
            )

        return httpx.Response(
            200,
            json={"job": {"job_id": "job_new", "status": "queued"}},
        )

    transport = httpx.MockTransport(handler)
    client = SirConvertALotV2Client(
        config=SirConvertALotConfig(base_url="https://example.test", api_key="k"),
        transport=transport,
    )

    async def run() -> None:
        record = await client.create_job(
            spec=ConversionJobSpec(source_filename="a.md", source_format="md", output_format="pdf"),
            content=b"# hello",
        )

        assert record.job_id == "job_new"
        assert record.status == "queued"

    asyncio.run(run())
    assert len(seen_idempotency_keys) == 2
    assert seen_idempotency_keys[1].startswith(seen_idempotency_keys[0] + "_rerun_")


def test_create_job_does_not_auto_rerun_on_nonterminal_replay() -> None:
    request_count = 0

    def handler(_: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(
            200,
            headers={"X-Idempotent-Replay": "true"},
            json={"job": {"job_id": "job_running", "status": "running"}},
        )

    transport = httpx.MockTransport(handler)
    client = SirConvertALotV2Client(
        config=SirConvertALotConfig(base_url="https://example.test", api_key="k"),
        transport=transport,
    )

    async def run() -> None:
        record = await client.create_job(
            spec=ConversionJobSpec(source_filename="a.md", source_format="md", output_format="pdf"),
            content=b"# hello",
        )

        assert record.job_id == "job_running"
        assert record.status == "running"

    asyncio.run(run())
    assert request_count == 1


def test_get_job_parses_nested_envelope() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return httpx.Response(200, json={"job": {"job_id": "job_123", "status": "running"}})

    transport = httpx.MockTransport(handler)
    client = SirConvertALotV2Client(
        config=SirConvertALotConfig(base_url="https://example.test", api_key="k"),
        transport=transport,
    )

    async def run() -> None:
        record = await client.get_job(job_id="job_123")
        assert record.job_id == "job_123"
        assert record.status == "running"

    asyncio.run(run())


def test_create_job_does_not_auto_rerun_when_not_replay() -> None:
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        assert request.method == "POST"
        return httpx.Response(
            202,
            headers={"X-Idempotent-Replay": "false"},
            json={"job": {"job_id": "job_failed", "status": "failed"}},
        )

    transport = httpx.MockTransport(handler)
    client = SirConvertALotV2Client(
        config=SirConvertALotConfig(base_url="https://example.test", api_key="k"),
        transport=transport,
    )

    async def run() -> None:
        record = await client.create_job(
            spec=ConversionJobSpec(source_filename="a.md", source_format="md", output_format="pdf"),
            content=b"# hello",
        )
        assert record.job_id == "job_failed"
        assert record.status == "failed"

    asyncio.run(run())
    assert request_count == 1
