from __future__ import annotations

import hashlib
from dataclasses import dataclass

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.infrastructure.exports.filesystem_exports_repo import (
    FileSystemExportsRepository,
)
from projektveckor_portal.interfaces.auth import CurrentUser
from projektveckor_portal.interfaces.conversion import (
    ConversionClient,
    ConversionJobSpec,
    SourceFormat,
)
from projektveckor_portal.interfaces.exports import (
    ExportCreateResult,
    ExportFormat,
    ExportRecord,
    ExportStatus,
)


@dataclass(frozen=True, slots=True)
class ExportsService:
    documents: DocumentsService
    repo: FileSystemExportsRepository
    converter: ConversionClient

    async def create_export(
        self,
        *,
        doc_path: str,
        export_format: ExportFormat,
        user: CurrentUser,
    ) -> ExportCreateResult:
        source = self.documents.get_document(doc_path=doc_path, user=user)
        if source is None:
            raise ValueError("Dokumentet hittades inte.")

        source_bytes, source_filename, source_format = _to_source_payload(
            doc_path=doc_path,
            source_format=source.meta.source_format,
            source_text=source.source,
        )
        export_id = _export_id(
            doc_path=doc_path,
            export_format=export_format,
            source_bytes=source_bytes,
        )

        existing = self.repo.get(export_id=export_id)
        if existing is None or existing.job_id is None:
            spec = ConversionJobSpec(
                source_filename=source_filename,
                source_format=source_format,
                output_format=export_format,
            )
            job = await self.converter.create_job(spec=spec, content=source_bytes)
            existing = ExportRecord(
                export_id=export_id,
                doc_path=doc_path,
                export_format=export_format,
                status=_map_status(job.status),
                job_id=job.job_id,
                artifact_filename=None,
                error_message=None,
            )
            self.repo.put(existing)

        await self._update_from_converter(export_id)
        updated = self.repo.get(export_id=export_id) or existing
        return ExportCreateResult(record=updated, artifact_available=updated.status == "succeeded")

    async def refresh(self, *, export_id: str) -> ExportRecord | None:
        record = self.repo.get(export_id=export_id)
        if record is None:
            return None
        await self._update_from_converter(export_id)
        return self.repo.get(export_id=export_id)

    def get(self, *, export_id: str) -> ExportRecord | None:
        return self.repo.get(export_id=export_id)

    async def _update_from_converter(self, export_id: str) -> None:
        record = self.repo.get(export_id=export_id)
        if record is None:
            return

        if record.status == "succeeded" and record.artifact_filename:
            return

        if record.job_id is None:
            # Jobb-id saknas (t.ex. om skapandet bröt). Markera failed för att synliggöra.
            self.repo.put(
                ExportRecord(
                    export_id=record.export_id,
                    doc_path=record.doc_path,
                    export_format=record.export_format,
                    status="failed",
                    job_id=None,
                    artifact_filename=record.artifact_filename,
                    error_message="Exportjobbet saknar job_id.",
                )
            )
            return

        try:
            job = await self.converter.get_job(job_id=record.job_id)
        except Exception as e:
            self.repo.put(
                ExportRecord(
                    export_id=record.export_id,
                    doc_path=record.doc_path,
                    export_format=record.export_format,
                    status="failed",
                    job_id=record.job_id,
                    artifact_filename=record.artifact_filename,
                    error_message=f"Kunde inte läsa jobbstatus: {e}",
                )
            )
            return

        status = _map_status(job.status)
        updated = ExportRecord(
            export_id=record.export_id,
            doc_path=record.doc_path,
            export_format=record.export_format,
            status=status,
            job_id=record.job_id,
            artifact_filename=record.artifact_filename,
            error_message=record.error_message,
        )
        self.repo.put(updated)

        if status != "succeeded":
            return

        if updated.artifact_filename:
            # Artifact finns redan sparad.
            return

        filename = f"artifact.{updated.export_format}"
        try:
            artifact = await self.converter.download_artifact(job_id=record.job_id)
        except Exception as e:
            self.repo.put(
                ExportRecord(
                    export_id=record.export_id,
                    doc_path=record.doc_path,
                    export_format=record.export_format,
                    status="failed",
                    job_id=record.job_id,
                    artifact_filename=None,
                    error_message=f"Kunde inte hämta filen: {e}",
                )
            )
            return

        self.repo.write_artifact(export_id=record.export_id, filename=filename, content=artifact)
        self.repo.put(
            ExportRecord(
                export_id=record.export_id,
                doc_path=record.doc_path,
                export_format=record.export_format,
                status="succeeded",
                job_id=record.job_id,
                artifact_filename=filename,
                error_message=None,
            )
        )


def _export_id(*, doc_path: str, export_format: ExportFormat, source_bytes: bytes) -> str:
    h = hashlib.sha256()
    h.update(doc_path.encode("utf-8"))
    h.update(export_format.encode("utf-8"))
    h.update(hashlib.sha256(source_bytes).digest())
    return f"exp_{h.hexdigest()[:32]}"


def _to_source_payload(
    *, doc_path: str, source_format: str, source_text: str
) -> tuple[bytes, str, SourceFormat]:
    slug = doc_path.rstrip("/").split("/")[-1] or "document"
    if source_format == "markdown":
        return source_text.encode("utf-8"), f"{slug}.md", "md"
    if source_format == "html":
        return source_text.encode("utf-8"), f"{slug}.html", "html"
    raise ValueError("Okänt källformat för dokumentet.")


def _map_status(status: str) -> ExportStatus:
    normalized = status.strip().lower()
    if normalized in {"queued", "running", "succeeded", "failed"}:
        return normalized  # type: ignore[return-value]
    if normalized in {"canceled", "cancelled"}:
        return "failed"
    return "failed"
