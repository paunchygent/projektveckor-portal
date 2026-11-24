from __future__ import annotations

import asyncio
import tomllib
from pathlib import Path

import pytest
import yaml
from dishka import make_async_container

from projektveckor_portal.di import container as container_module
from projektveckor_portal.infrastructure.conversion.sir_convert_a_lot_v2_client import (
    SirConvertALotV2Client,
)
from projektveckor_portal.interfaces.conversion import ConversionClient
from projektveckor_portal.settings import Settings

REPO_ROOT = Path(__file__).resolve().parents[1]
KEY_NAME = "SIR_CONVERT_A_LOT_V2_API_KEY"
PLACEHOLDER_URL = "http://example.invalid"
PLACEHOLDER_KEY = "placeholder"

_LEGACY_KEY_NAMES = [
    "PVP_SIR_CONVERT_A_LOT_API_KEY",
    "PVP_SIR_CONVERT_A_LOT_V2_API_KEY",
    "SIR_CONVERT_A_LOT_API_KEY",
]


@pytest.fixture(autouse=True)
def _clean_sir_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in [KEY_NAME, "PVP_SIR_CONVERT_A_LOT_BASE_URL", *_LEGACY_KEY_NAMES]:
        monkeypatch.delenv(name, raising=False)


def _build_converter(
    monkeypatch: pytest.MonkeyPatch, settings: Settings
) -> ConversionClient | None:
    monkeypatch.setattr(container_module, "settings", settings)

    async def resolve() -> ConversionClient | None:
        container = make_async_container(container_module._PortalProvider())
        try:
            converter: ConversionClient | None = await container.get(ConversionClient | None)
            return converter
        finally:
            await container.close()

    return asyncio.run(resolve())


def _write_env_file_with_key(directory: Path) -> None:
    (directory / ".env").write_text(
        f"PVP_SIR_CONVERT_A_LOT_BASE_URL={PLACEHOLDER_URL}\n{KEY_NAME}={PLACEHOLDER_KEY}\n"
    )


def test_settings_loads_configuration_from_dotenv_and_has_no_key_field(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_env_file_with_key(tmp_path)
    monkeypatch.chdir(tmp_path)
    settings = Settings()
    assert settings.sir_convert_a_lot_base_url == PLACEHOLDER_URL
    assert not any("api_key" in field for field in Settings.model_fields)
    assert PLACEHOLDER_KEY not in settings.model_dump_json()


def test_settings_ignores_legacy_key_names_in_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in _LEGACY_KEY_NAMES:
        monkeypatch.setenv(name, PLACEHOLDER_KEY)
    assert PLACEHOLDER_KEY not in Settings().model_dump_json()


def test_converter_is_not_built_from_a_key_in_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_env_file_with_key(tmp_path)
    monkeypatch.chdir(tmp_path)
    settings = Settings()
    assert settings.sir_convert_a_lot_base_url == PLACEHOLDER_URL
    assert _build_converter(monkeypatch, settings) is None


def test_converter_receives_the_key_from_the_process_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(KEY_NAME, PLACEHOLDER_KEY)
    settings = Settings(sir_convert_a_lot_base_url=PLACEHOLDER_URL)
    converter = _build_converter(monkeypatch, settings)
    assert isinstance(converter, SirConvertALotV2Client)
    assert converter._config.api_key == PLACEHOLDER_KEY
    assert converter._config.base_url == PLACEHOLDER_URL


def test_host_serve_runs_through_agent_secrets_and_serve_lan_does_not() -> None:
    parsed = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    scripts = parsed["tool"]["pdm"]["scripts"]
    assert scripts["serve"] == (
        "agent-secrets run --set projektveckor-portal-prod -- "
        "uvicorn projektveckor_portal.app:app --host 127.0.0.1 --port 8000"
    )
    assert "agent-secrets" not in scripts["serve:lan"]


def _load_yaml(name: str) -> dict[str, object]:
    loaded = yaml.safe_load((REPO_ROOT / name).read_text())
    assert isinstance(loaded, dict)
    return loaded


def _web_service(compose: dict[str, object]) -> dict[str, object]:
    services = compose["services"]
    assert isinstance(services, dict)
    web = services["web"]
    assert isinstance(web, dict)
    return web


def _key_locations(node: object, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}/{key}"
            if KEY_NAME in str(key):
                found.append(child)
            found.extend(_key_locations(value, child))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(_key_locations(value, f"{path}/{index}"))
    elif KEY_NAME in str(node):
        found.append(path)
    return sorted(set(found))


def test_compose_files_deliver_the_key_only_through_the_overlay_web_environment() -> None:
    base = _load_yaml("compose.prod.yaml")
    overlay = _load_yaml("compose.secrets.prod.yaml")

    assert _key_locations(base) == []
    assert _key_locations(overlay) == [f"/services/web/environment/{KEY_NAME}"]
    assert _web_service(base)["env_file"] == [".env"]
    assert "env_file" not in _web_service(overlay)
