from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import yaml

from projektveckor_portal.domain.doc_paths import DocPath
from projektveckor_portal.interfaces.documents import (
    DocumentMeta,
    DocumentRecord,
    DocumentRepository,
)


class FileSystemDocumentRepository(DocumentRepository):
    def __init__(self, *, root: Path) -> None:
        self._root = root

    def list_metas(self, *, prefix: str | None = None) -> list[DocumentMeta]:
        base = self._root
        if prefix:
            base = self._root / DocPath.parse(prefix).value
        if not base.exists():
            return []

        metas: list[DocumentMeta] = []
        for meta_file in sorted(base.rglob("meta.yaml")):
            try:
                doc_dir = meta_file.parent
                doc_path = str(doc_dir.relative_to(self._root)).replace("\\", "/")
                meta = self._read_meta(meta_file, doc_path=doc_path)
                metas.append(meta)
            except Exception:
                continue
        return metas

    def get_record(self, *, doc_path: str) -> DocumentRecord | None:
        parsed = DocPath.parse(doc_path).value
        doc_dir = self._root / parsed
        meta_file = doc_dir / "meta.yaml"
        if not meta_file.exists():
            return None

        meta = self._read_meta(meta_file, doc_path=parsed)
        source_file = doc_dir / ("source.md" if meta.source_format == "markdown" else "source.html")
        if not source_file.exists():
            source = ""
        else:
            source = source_file.read_text(encoding="utf-8")

        return DocumentRecord(meta=meta, source=source)

    def put_record(self, record: DocumentRecord) -> None:
        parsed = DocPath.parse(record.meta.doc_path).value
        doc_dir = self._root / parsed
        doc_dir.mkdir(parents=True, exist_ok=True)

        meta_file = doc_dir / "meta.yaml"
        meta_file.write_text(self._dump_meta(record.meta), encoding="utf-8")

        source_filename = "source.md" if record.meta.source_format == "markdown" else "source.html"
        source_file = doc_dir / source_filename
        source_file.write_text(record.source, encoding="utf-8")

    def _read_meta(self, meta_file: Path, *, doc_path: str) -> DocumentMeta:
        raw = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            raw = {}

        title = str(raw.get("title", "")).strip() or doc_path
        visibility = str(raw.get("visibility", "public")).strip()
        if visibility not in {"public", "teacher"}:
            visibility = "public"

        source_format = str(raw.get("source_format", "markdown")).strip()
        if source_format not in {"markdown", "html"}:
            source_format = "markdown"

        return DocumentMeta(
            doc_path=doc_path,
            title=title,
            visibility=visibility,  # type: ignore[arg-type]
            source_format=source_format,  # type: ignore[arg-type]
        )

    def _dump_meta(self, meta: DocumentMeta) -> str:
        data = asdict(meta)
        dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        return str(dumped).strip() + "\n"
