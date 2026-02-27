from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from projektveckor_portal.interfaces.exports import ExportRecord


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


def _from_dict(payload: dict[str, Any]) -> ExportRecord:
    return ExportRecord(
        export_id=str(payload.get("export_id", "")).strip(),
        doc_path=str(payload.get("doc_path", "")).strip(),
        export_format=str(payload.get("export_format", "")).strip(),  # type: ignore[arg-type]
        status=str(payload.get("status", "")).strip(),  # type: ignore[arg-type]
        job_id=str(payload.get("job_id", "")).strip() or None,
        artifact_filename=str(payload.get("artifact_filename", "")).strip() or None,
        error_message=str(payload.get("error_message", "")).strip() or None,
    )

