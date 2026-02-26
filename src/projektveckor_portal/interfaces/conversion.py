from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

OutputFormat = Literal["pdf", "docx"]
SourceFormat = Literal["md", "html", "pdf"]


@dataclass(frozen=True, slots=True)
class ConversionJobSpec:
    source_filename: str
    source_format: SourceFormat
    output_format: OutputFormat


@dataclass(frozen=True, slots=True)
class ConversionJobRecord:
    job_id: str
    status: str


class ConversionClient(Protocol):
    async def create_job(
        self, *, spec: ConversionJobSpec, content: bytes
    ) -> ConversionJobRecord: ...
    async def get_job(self, *, job_id: str) -> ConversionJobRecord: ...
    async def download_artifact(self, *, job_id: str) -> bytes: ...
