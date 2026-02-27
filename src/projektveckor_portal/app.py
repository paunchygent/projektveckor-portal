from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from projektveckor_portal.di.container import setup_di
from projektveckor_portal.settings import settings
from projektveckor_portal.web.auth_routes import router as auth_router
from projektveckor_portal.web.documents_routes import router as documents_router
from projektveckor_portal.web.exports_routes import router as exports_router


def create_app() -> FastAPI:
    app = FastAPI(title="Projektveckor Portal", version=settings.service_version)

    @app.get("/healthz", include_in_schema=False)
    def healthz() -> JSONResponse:
        return JSONResponse(
            {"status": "ok", "service": settings.service_name, "version": settings.service_version}
        )

    setup_di(app)
    app.include_router(auth_router)
    app.include_router(documents_router)
    app.include_router(exports_router)
    _configure_spa(app)
    return app


def _configure_spa(app: FastAPI) -> None:
    dist_dir = _repo_root() / "frontend" / "dist"
    if not dist_dir.exists():
        return

    app.mount("/assets", StaticFiles(directory=str(dist_dir / "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    def spa_index() -> FileResponse:
        return FileResponse(dist_dir / "index.html")

    @app.get("/{path:path}", include_in_schema=False)
    def spa_fallback(path: str) -> FileResponse:
        target = dist_dir / path
        if target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(dist_dir / "index.html")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


app = create_app()
