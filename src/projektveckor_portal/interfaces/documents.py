from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

Visibility = Literal["public", "teacher"]
SourceFormat = Literal["markdown", "html"]


@dataclass(frozen=True, slots=True)
class DocumentMeta:
    doc_path: str
    title: str
    visibility: Visibility
    source_format: SourceFormat


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    meta: DocumentMeta
    source: str


class DocumentRepository(Protocol):
    def list_metas(self, *, prefix: str | None = None) -> list[DocumentMeta]: ...
    def get_record(self, *, doc_path: str) -> DocumentRecord | None: ...
    def put_record(self, record: DocumentRecord) -> None: ...
