from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ExportFormat = Literal["pdf", "docx"]
ExportStatus = Literal["queued", "running", "succeeded", "failed"]


@dataclass(frozen=True, slots=True)
class ExportRecord:
    export_id: str
    doc_path: str
    export_format: ExportFormat
    status: ExportStatus
    job_id: str | None = None
    artifact_filename: str | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class ExportCreateResult:
    record: ExportRecord
    artifact_available: bool
