from __future__ import annotations

import asyncio
from pathlib import Path

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.application.exports_service import ExportsService, _export_id
from projektveckor_portal.infrastructure.documents.filesystem_repo import (
    FileSystemDocumentRepository,
)
from projektveckor_portal.infrastructure.exports.filesystem_exports_repo import (
    FileSystemExportsRepository,
)
from projektveckor_portal.interfaces.auth import CurrentUser
from projektveckor_portal.interfaces.conversion import ConversionJobRecord, ConversionJobSpec
from projektveckor_portal.interfaces.documents import DocumentMeta, DocumentRecord
from projektveckor_portal.interfaces.exports import ExportRecord


def test_create_export_resubmits_when_existing_export_is_failed(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    exports_root = tmp_path / "exports"

    docs_repo = FileSystemDocumentRepository(root=docs_root)
    docs_service = DocumentsService(docs_repo)
    exports_repo = FileSystemExportsRepository(root=exports_root)

    doc_path = "fn-rollspel/v43/borja-har"
    docs_service.put_document(
        record=DocumentRecord(
            meta=DocumentMeta(
                doc_path=doc_path,
                title="Test",
                visibility="teacher",
                source_format="markdown",
            ),
            source="# hello",
        )
    )

    user = CurrentUser(user_id="u1", roles=frozenset({"teacher"}))

    # Pre-create a failed export record (same deterministic export_id).
    source_bytes = b"# hello"
    export_id = _export_id(doc_path=doc_path, export_format="pdf", source_bytes=source_bytes)
    exports_repo.put(
        ExportRecord(
            export_id=export_id,
            doc_path=doc_path,
            export_format="pdf",
            status="failed",
            job_id="job_old",
            artifact_filename="artifact.pdf",
            error_message="old failure",
        )
    )

    class StubConverter:
        def __init__(self) -> None:
            self.create_calls: list[ConversionJobSpec] = []
            self.get_calls: list[str] = []

        async def create_job(
            self, *, spec: ConversionJobSpec, content: bytes
        ) -> ConversionJobRecord:
            self.create_calls.append(spec)
            return ConversionJobRecord(job_id="job_new", status="queued")

        async def get_job(self, *, job_id: str) -> ConversionJobRecord:
            self.get_calls.append(job_id)
            return ConversionJobRecord(job_id=job_id, status="running")

        async def download_artifact(self, *, job_id: str) -> bytes:
            raise AssertionError("download_artifact should not run for non-succeeded jobs")

    converter = StubConverter()
    service = ExportsService(documents=docs_service, repo=exports_repo, converter=converter)

    async def run() -> None:
        result = await service.create_export(doc_path=doc_path, export_format="pdf", user=user)
        assert result.record.export_id == export_id
        assert result.record.job_id == "job_new"
        assert result.record.status == "running"
        assert result.record.error_message is None
        assert result.record.artifact_filename is None
        assert result.artifact_available is False

    asyncio.run(run())

    assert len(converter.create_calls) == 1
    assert converter.get_calls == ["job_new"]
