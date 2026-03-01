from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Mapping

from projektveckor_portal.interfaces.exports import ExportFormat, ExportRecord, ExportStatus


class FileSystemExportsRepository:
    def __init__(self, *, root: Path) -> None:
        self._root = root

    def get(self, *, export_id: str) -> ExportRecord | None:
        path = self._meta_path(export_id=export_id)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return _from_dict(payload)

    def put(self, record: ExportRecord) -> None:
        self._ensure_export_dir(export_id=record.export_id)
        path = self._meta_path(export_id=record.export_id)
        path.write_text(json.dumps(asdict(record), ensure_ascii=False, indent=2), encoding="utf-8")

    def write_artifact(self, *, export_id: str, filename: str, content: bytes) -> Path:
        export_dir = self._ensure_export_dir(export_id=export_id)
        target = export_dir / filename
        target.write_bytes(content)
        return target

    def artifact_path(self, *, export_id: str, filename: str) -> Path:
        return self._ensure_export_dir(export_id=export_id) / filename

    def _ensure_export_dir(self, *, export_id: str) -> Path:
        export_dir = self._root / export_id
        export_dir.mkdir(parents=True, exist_ok=True)
        return export_dir

    def _meta_path(self, *, export_id: str) -> Path:
        return self._root / export_id / "meta.json"


def _from_dict(payload: Mapping[str, object]) -> ExportRecord:
    export_format_raw = _required_str(payload, "export_format")
    if export_format_raw == "pdf":
        export_format: ExportFormat = "pdf"
    elif export_format_raw == "docx":
        export_format = "docx"
    else:
        export_format = "pdf"

    status_raw = _required_str(payload, "status").strip().lower()
    if status_raw == "queued":
        status: ExportStatus = "queued"
    elif status_raw == "running":
        status = "running"
    elif status_raw == "succeeded":
        status = "succeeded"
    else:
        status = "failed"

    return ExportRecord(
        export_id=_required_str(payload, "export_id"),
        doc_path=_required_str(payload, "doc_path"),
        export_format=export_format,
        status=status,
        job_id=_optional_str(payload, "job_id"),
        artifact_filename=_optional_str(payload, "artifact_filename"),
        error_message=_optional_str(payload, "error_message"),
    )


def _required_str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _optional_str(payload: Mapping[str, object], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    stripped = str(value).strip()
    return stripped or None
