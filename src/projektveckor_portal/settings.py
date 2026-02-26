from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PVP_", env_file=".env", extra="ignore")

    environment: str = "dev"
    service_name: str = "projektveckor-portal"
    service_version: str = "0.1.0"

    docs_root: Path = Path("data/doclib")
    exports_root: Path = Path("data/exports")

    identity_introspect_url: str | None = None

    sir_convert_a_lot_base_url: str | None = None
    sir_convert_a_lot_api_key: str | None = None


settings = Settings()
