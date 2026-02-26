from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.interfaces.documents import DocumentMeta, DocumentRecord
from projektveckor_portal.web.dependencies import get_current_user_optional, require_teacher

router = APIRouter()


class PutDocumentRequest(BaseModel):
    title: str = Field(min_length=1)
    visibility: Literal["public", "teacher"] = "public"
    source_format: Literal["markdown", "html"] = "markdown"
    source: str = Field(default="")


def _service_from_request(request: Request) -> DocumentsService:
    service = getattr(request.app.state, "documents_service", None)
    if not isinstance(service, DocumentsService):
        raise RuntimeError("DocumentsService is not configured")
    return service


@router.get("/api/documents")
async def list_documents(request: Request, prefix: str | None = None) -> JSONResponse:
    service = _service_from_request(request)
    user = await get_current_user_optional(request)
    metas = service.list_documents(prefix=prefix, user=user)
    return JSONResponse([_meta_to_dict(m) for m in metas])


@router.get("/api/documents/{doc_path:path}")
async def get_document(request: Request, doc_path: str) -> JSONResponse:
    service = _service_from_request(request)
    user = await get_current_user_optional(request)
    record = service.get_document(doc_path=doc_path, user=user)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dokumentet hittades inte.",
        )
    return JSONResponse({"meta": _meta_to_dict(record.meta), "source": record.source})


@router.put("/api/admin/documents/{doc_path:path}")
async def put_document(
    request: Request,
    doc_path: str,
    payload: PutDocumentRequest,
    _: object = Depends(require_teacher),
) -> JSONResponse:
    service = _service_from_request(request)
    record = DocumentRecord(
        meta=DocumentMeta(
            doc_path=doc_path,
            title=payload.title,
            visibility=payload.visibility,
            source_format=payload.source_format,
        ),
        source=payload.source,
    )
    service.put_document(record=record)
    return JSONResponse({"ok": True})


@router.get("/d/{doc_path:path}", include_in_schema=False)
async def preview_document(request: Request, doc_path: str) -> HTMLResponse:
    service = _service_from_request(request)
    user = await get_current_user_optional(request)
    preview = service.render_preview(doc_path=doc_path, user=user)
    if preview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dokumentet hittades inte.",
        )
    return HTMLResponse(preview.html)


@router.get("/d", include_in_schema=False)
async def preview_index(request: Request, prefix: str | None = None) -> HTMLResponse:
    service = _service_from_request(request)
    user = await get_current_user_optional(request)
    metas = service.list_documents(prefix=prefix, user=user)

    items = "\n".join(
        (
            f'<li><a href="/d/{m.doc_path}">{m.title}</a> '
            f'<span style="color:#6b7280">— {m.doc_path}</span></li>'
        )
        for m in metas
    )
    html = f"""<!doctype html>
<html lang="sv">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dokument</title>
    <style>
      :root {{
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
      .meta {{ color: var(--muted); font-size: 14px; }}
    </style>
  </head>
  <body>
    <header>
      <div class="wrap">
        <div class="crumbs">
          <a href="/">Projektveckor</a> / <span>Dokument</span>
        </div>
        <h1>Dokument</h1>
      </div>
    </header>
    <main>
      <div class="wrap">
        <h2>Översikt</h2>
        <p>Här är dokument som portalen hostar.</p>
        <ul>
          {items if items else '<li>Inga dokument ännu.</li>'}
        </ul>
      </div>
    </main>
  </body>
</html>
"""
    return HTMLResponse(html)


def _meta_to_dict(meta: DocumentMeta) -> dict[str, object]:
    return {
        "doc_path": meta.doc_path,
        "title": meta.title,
        "visibility": meta.visibility,
        "source_format": meta.source_format,
        "preview_url": f"/d/{meta.doc_path}",
    }
