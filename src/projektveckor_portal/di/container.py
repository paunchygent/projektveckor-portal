from __future__ import annotations

from pathlib import Path

from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import FastAPI

from projektveckor_portal.application.documents_service import DocumentsService
from projektveckor_portal.application.exports_service import ExportsService
from projektveckor_portal.infrastructure.auth.identity_http_client import (
    IdentityConfig,
    IdentityHttpClient,
)
from projektveckor_portal.infrastructure.auth.identity_introspection import (
    IdentityIntrospectionAuthenticator,
    IdentityIntrospectionConfig,
)
from projektveckor_portal.infrastructure.conversion.sir_convert_a_lot_v2_client import (
    SirConvertALotConfig,
    SirConvertALotV2Client,
)
from projektveckor_portal.infrastructure.documents.filesystem_repo import (
    FileSystemDocumentRepository,
)
from projektveckor_portal.infrastructure.exports.filesystem_exports_repo import (
    FileSystemExportsRepository,
)
from projektveckor_portal.interfaces.auth import Authenticator, IdentityClient
from projektveckor_portal.interfaces.conversion import ConversionClient
from projektveckor_portal.interfaces.documents import DocumentRepository
from projektveckor_portal.settings import Settings, settings


def setup_di(app: FastAPI) -> None:
    app.router.route_class = DishkaRoute
    container = make_async_container(_PortalProvider())
    setup_dishka(app=app, container=container)


class _PortalProvider(Provider):
    @provide(scope=Scope.APP)
    def _settings(self) -> Settings:
        return settings

    @provide(scope=Scope.APP)
    def _repo_root(self) -> Path:
        # src/projektveckor_portal/di/container.py -> repo root
        return Path(__file__).resolve().parents[3]

    @provide(scope=Scope.APP)
    def _documents_repo(self, repo_root: Path, settings: Settings) -> DocumentRepository:
        root = repo_root / settings.docs_root
        return FileSystemDocumentRepository(root=root)

    @provide(scope=Scope.APP)
    def _documents_service(self, repo: DocumentRepository) -> DocumentsService:
        return DocumentsService(repo)

    @provide(scope=Scope.APP)
    def _authenticator(self, settings: Settings) -> Authenticator | None:
        introspect_url = settings.identity_introspect_url
        if not introspect_url and settings.identity_base_url:
            introspect_url = f"{settings.identity_base_url.rstrip('/')}/v1/auth/introspect"
        if not introspect_url:
            return None
        return IdentityIntrospectionAuthenticator(
            config=IdentityIntrospectionConfig(introspect_url=introspect_url)
        )

    @provide(scope=Scope.APP)
    def _identity_client(self, settings: Settings) -> IdentityClient | None:
        if not settings.identity_base_url:
            return None
        return IdentityHttpClient(config=IdentityConfig(base_url=settings.identity_base_url))

    @provide(scope=Scope.APP)
    def _conversion_client(self, settings: Settings) -> ConversionClient | None:
        if not settings.sir_convert_a_lot_base_url or not settings.sir_convert_a_lot_api_key:
            return None
        return SirConvertALotV2Client(
            config=SirConvertALotConfig(
                base_url=settings.sir_convert_a_lot_base_url,
                api_key=settings.sir_convert_a_lot_api_key,
            )
        )

    @provide(scope=Scope.APP)
    def _exports_repo(self, repo_root: Path, settings: Settings) -> FileSystemExportsRepository:
        root = repo_root / settings.exports_root
        return FileSystemExportsRepository(root=root)

    @provide(scope=Scope.APP)
    def _exports_service(
        self,
        documents: DocumentsService,
        repo: FileSystemExportsRepository,
        converter: ConversionClient | None,
    ) -> ExportsService | None:
        if converter is None:
            return None
        return ExportsService(documents=documents, repo=repo, converter=converter)
