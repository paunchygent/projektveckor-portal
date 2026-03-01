from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from projektveckor_portal.domain.doc_paths import DocPath

Visibility = Literal["public", "teacher"]
SourceFormat = Literal["markdown", "html"]


@dataclass(frozen=True, slots=True)
class Document:
    doc_path: DocPath
    title: str
    visibility: Visibility
    source_format: SourceFormat
    source: str
