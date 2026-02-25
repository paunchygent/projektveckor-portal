from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PVP_", env_file=".env", extra="ignore")

    environment: str = "dev"
    service_name: str = "projektveckor-portal"
    service_version: str = "0.1.0"


settings = Settings()

