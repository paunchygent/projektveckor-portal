from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

_SAFE_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class DocPath:
    value: str

    @staticmethod
    def parse(raw: str) -> "DocPath":
        compact = raw.strip().strip("/")
        if compact == "":
            raise ValueError("doc_path must be non-empty")

        parts = [p for p in PurePosixPath(compact).parts if p not in {"", "."}]
        if not parts:
            raise ValueError("doc_path must have at least one segment")
        if any(part == ".." for part in parts):
            raise ValueError("doc_path must not contain '..'")
        if any(not _SAFE_SEGMENT_RE.match(part) for part in parts):
            raise ValueError("doc_path must use lowercase a-z0-9 segments with '-' only")

        normalized = "/".join(parts)
        return DocPath(normalized)
