from __future__ import annotations

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict

from projektveckor_portal.application.exports_service import ExportsService
from projektveckor_portal.interfaces.auth import CurrentUser
from projektveckor_portal.interfaces.exports import ExportFormat, ExportRecord
from projektveckor_portal.web.dependencies import require_csrf, require_teacher

router = APIRouter(prefix="/api/admin", tags=["exports"], route_class=DishkaRoute)


class CreateExportRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    format: ExportFormat


def _to_dict(record: ExportRecord) -> dict[str, object]:
    return {
        "export_id": record.export_id,
        "doc_path": record.doc_path,
        "format": record.export_format,
        "status": record.status,
        "job_id": record.job_id,
        "artifact_url": f"/api/admin/exports/{record.export_id}/artifact"
        if record.status == "succeeded" and record.artifact_filename
        else None,
        "error_message": record.error_message,
    }


@router.post(
    "/documents/{doc_path:path}/exports",
    dependencies=[Depends(require_csrf)],
)
async def create_export(
    doc_path: str,
    payload: CreateExportRequest,
    service: FromDishka[ExportsService | None],
    user: CurrentUser = Depends(require_teacher),
) -> JSONResponse:
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Export är inte konfigurerat i den här miljön.",
        )
    try:
        result = await service.create_export(
            doc_path=doc_path,
            export_format=payload.format,
            user=user,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from None
    return JSONResponse(_to_dict(result.record), status_code=status.HTTP_202_ACCEPTED)


@router.get("/exports/{export_id}")
async def get_export(
    export_id: str,
    service: FromDishka[ExportsService | None],
    _: object = Depends(require_teacher),
) -> JSONResponse:
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Export är inte konfigurerat i den här miljön.",
        )
    record = await service.refresh(export_id=export_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exporten hittades inte.")
    return JSONResponse(_to_dict(record))


@router.get("/exports/{export_id}/artifact")
async def get_export_artifact(
    export_id: str,
    service: FromDishka[ExportsService | None],
    _: object = Depends(require_teacher),
) -> FileResponse:
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Export är inte konfigurerat i den här miljön.",
        )
    record = service.get(export_id=export_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exporten hittades inte.")
    if record.status != "succeeded" or not record.artifact_filename:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exporten är inte klar ännu.",
        )
    path = service.repo.artifact_path(export_id=export_id, filename=record.artifact_filename)
    if not path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filen hittades inte.")
    return FileResponse(path)
