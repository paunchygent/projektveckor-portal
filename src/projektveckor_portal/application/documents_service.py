from __future__ import annotations

from dataclasses import dataclass

import markdown

from projektveckor_portal.domain.doc_paths import DocPath
from projektveckor_portal.domain.documents import Document
from projektveckor_portal.interfaces.auth import CurrentUser
from projektveckor_portal.interfaces.documents import (
    DocumentMeta,
    DocumentRecord,
    DocumentRepository,
)


@dataclass(frozen=True, slots=True)
class DocumentPreview:
    title: str
    html: str


class DocumentsService:
    def __init__(self, repo: DocumentRepository) -> None:
        self._repo = repo

    def list_documents(self, *, prefix: str | None, user: CurrentUser | None) -> list[DocumentMeta]:
        metas = self._repo.list_metas(prefix=prefix)
        if user is not None and user.is_teacher:
            return metas
        return [m for m in metas if m.visibility == "public"]

    def get_document(self, *, doc_path: str, user: CurrentUser | None) -> DocumentRecord | None:
        parsed = DocPath.parse(doc_path).value
        record = self._repo.get_record(doc_path=parsed)
        if record is None:
            return None
        if record.meta.visibility == "public":
            return record
        if user is not None and user.is_teacher:
            return record
        return None

    def put_document(self, *, record: DocumentRecord) -> None:
        parsed = DocPath.parse(record.meta.doc_path).value
        normalized = DocumentRecord(
            meta=DocumentMeta(
                doc_path=parsed,
                title=record.meta.title.strip(),
                visibility=record.meta.visibility,
                source_format=record.meta.source_format,
            ),
            source=record.source,
        )
        self._repo.put_record(normalized)

    def render_preview(self, *, doc_path: str, user: CurrentUser | None) -> DocumentPreview | None:
        record = self.get_document(doc_path=doc_path, user=user)
        if record is None:
            return None

        document = Document(
            doc_path=DocPath.parse(record.meta.doc_path),
            title=record.meta.title,
            visibility=record.meta.visibility,
            source_format=record.meta.source_format,
            source=record.source,
        )
        html_body = self._render_document_body(document)
        html = self._wrap_html(title=document.title, body_html=html_body)
        return DocumentPreview(title=document.title, html=html)

    def _render_document_body(self, document: Document) -> str:
        if document.source_format == "html":
            return document.source

        rendered = markdown.markdown(
            document.source,
            extensions=["extra", "tables"],
            output_format="html",
        )
        return str(rendered)

    def _wrap_html(self, *, title: str, body_html: str) -> str:
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"""<!doctype html>
<html lang="sv">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <style>
      :root {{
        color-scheme: light;
        --max: 920px;
        --fg: #111827;
        --muted: #6b7280;
        --bg: #ffffff;
        --panel: #f8fafc;
        --border: #e5e7eb;
        --link: #2563eb;
      }}
      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: var(--fg);
        background: var(--bg);
      }}
      header {{
        border-bottom: 1px solid var(--border);
        background: var(--panel);
      }}
      .wrap {{ max-width: var(--max); margin: 0 auto; padding: 16px; }}
      .crumbs {{ font-size: 14px; color: var(--muted); }}
      .crumbs a {{ color: var(--link); text-decoration: none; }}
      h1 {{ margin: 8px 0 0; font-size: 28px; }}
      main .wrap {{ padding: 24px 16px 48px; }}
      a {{ color: var(--link); }}
      pre {{
        overflow: auto;
        padding: 12px;
        border: 1px solid var(--border);
        background: #0b1020;
        color: #e5e7eb;
        border-radius: 8px;
      }}
      code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid var(--border); padding: 8px; text-align: left; }}
      blockquote {{
        margin: 16px 0;
        padding: 8px 12px;
        border-left: 4px solid var(--border);
        color: var(--muted);
      }}
    </style>
  </head>
  <body>
    <header>
      <div class="wrap">
        <div class="crumbs">
          <a href="/">Projektveckor</a> / <span>Dokument</span>
        </div>
        <h1>{safe_title}</h1>
      </div>
    </header>
    <main>
      <div class="wrap">
        {body_html}
      </div>
    </main>
  </body>
</html>
"""
