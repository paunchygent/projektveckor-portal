from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.infrastructure.auth.identity_introspection import (
    IdentityIntrospectionAuthenticator,
    IdentityIntrospectionConfig,
)
from projektveckor_portal.infrastructure.documents.filesystem_repo import (
    FileSystemDocumentRepository,
)
from projektveckor_portal.settings import settings
from projektveckor_portal.web.dependencies import AppDependencies
from projektveckor_portal.web.documents_routes import router as documents_router


def create_app() -> FastAPI:
    app = FastAPI(title="Projektveckor Portal", version=settings.service_version)

    @app.get("/healthz", include_in_schema=False)
    def healthz() -> JSONResponse:
        return JSONResponse(
            {"status": "ok", "service": settings.service_name, "version": settings.service_version}
        )

    _configure_dependencies(app)
    app.include_router(documents_router)
    _configure_spa(app)
    return app


def _configure_dependencies(app: FastAPI) -> None:
    docs_root = _repo_root() / settings.docs_root
    repo = FileSystemDocumentRepository(root=docs_root)
    app.state.documents_service = DocumentsService(repo)

    authenticator = None
    if settings.identity_introspect_url:
        authenticator = IdentityIntrospectionAuthenticator(
            config=IdentityIntrospectionConfig(introspect_url=settings.identity_introspect_url)
        )
    app.state.deps = AppDependencies(authenticator=authenticator)


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

