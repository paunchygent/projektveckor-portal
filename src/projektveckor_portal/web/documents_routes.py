from __future__ import annotations

from typing import Literal

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.interfaces.auth import CurrentUser
from projektveckor_portal.interfaces.documents import DocumentMeta, DocumentRecord
from projektveckor_portal.web.dependencies import (
    get_current_user_optional,
    require_csrf,
    require_teacher,
)
from projektveckor_portal.web.views import render_preview_index

router = APIRouter(route_class=DishkaRoute)


class PutDocumentRequest(BaseModel):
    title: str = Field(min_length=1)
    visibility: Literal["public", "teacher"] = "public"
    source_format: Literal["markdown", "html"] = "markdown"
    source: str = Field(default="")


@router.get("/api/documents")
async def list_documents(
    service: FromDishka[DocumentsService],
    prefix: str | None = None,
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> JSONResponse:
    metas = service.list_documents(prefix=prefix, user=user)
    return JSONResponse([_meta_to_dict(m) for m in metas])


@router.get("/api/documents/{doc_path:path}")
async def get_document(
    doc_path: str,
    service: FromDishka[DocumentsService],
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> JSONResponse:
    record = service.get_document(doc_path=doc_path, user=user)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dokumentet hittades inte.",
        )
    return JSONResponse({"meta": _meta_to_dict(record.meta), "source": record.source})


@router.put("/api/admin/documents/{doc_path:path}")
async def put_document(
    doc_path: str,
    payload: PutDocumentRequest,
    service: FromDishka[DocumentsService],
    _: object = Depends(require_teacher),
    __: object = Depends(require_csrf),
) -> JSONResponse:
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
async def preview_document(
    doc_path: str,
    service: FromDishka[DocumentsService],
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> HTMLResponse:
    preview = service.render_preview(doc_path=doc_path, user=user)
    if preview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dokumentet hittades inte.",
        )
    return HTMLResponse(preview.html)


@router.get("/d", include_in_schema=False)
async def preview_index(
    service: FromDishka[DocumentsService],
    prefix: str | None = None,
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> HTMLResponse:
    metas = service.list_documents(prefix=prefix, user=user)

    items = "\n".join(
        (
            f'<li><a href="/d/{m.doc_path}">{m.title}</a> '
            f'<span style="color:#6b7280">— {m.doc_path}</span></li>'
        )
        for m in metas
    )
    html = render_preview_index(items)
    return HTMLResponse(html)


def _meta_to_dict(meta: DocumentMeta) -> dict[str, object]:
    return {
        "doc_path": meta.doc_path,
        "title": meta.title,
        "visibility": meta.visibility,
        "source_format": meta.source_format,
        "preview_url": f"/d/{meta.doc_path}",
    }
