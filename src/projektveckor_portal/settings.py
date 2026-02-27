from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PVP_", env_file=".env", extra="ignore")

    environment: str = "dev"
    service_name: str = "projektveckor-portal"
    service_version: str = "0.1.0"

    docs_root: Path = Path("data/doclib")
    exports_root: Path = Path("data/exports")

    # Identity (HuleEdu)
    identity_base_url: str | None = None
    identity_introspect_url: str | None = None

    sir_convert_a_lot_base_url: str | None = None
    sir_convert_a_lot_api_key: str | None = None

    # Auth cookies (portal-owned, short-term BFF)
    auth_access_cookie_name: str = "pvp_access_token"
    auth_refresh_cookie_name: str = "pvp_refresh_token"
    csrf_cookie_name: str = "pvp_csrf_token"

    cookie_secure: bool = False
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"


settings = Settings()
