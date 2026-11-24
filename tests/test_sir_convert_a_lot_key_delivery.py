from __future__ import annotations

import asyncio
import json
import shlex
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
from projektveckor_portal.settings import Settings, load_settings

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


def _write_settings_files(directory: Path) -> None:
    (directory / ".env").write_text("PVP_SERVICE_NAME=prod-name\nPVP_COOKIE_SAMESITE=strict\n")
    (directory / ".env.dev").write_text("PVP_SERVICE_NAME=dev-name\nPVP_COOKIE_SAMESITE=none\n")


def test_settings_file_selector_reads_the_dev_file_and_not_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_settings_files(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PVP_SERVICE_NAME", raising=False)
    monkeypatch.delenv("PVP_COOKIE_SAMESITE", raising=False)
    monkeypatch.setenv("PVP_SETTINGS_FILE", ".env.dev")
    settings = load_settings()
    assert settings.service_name == "dev-name"
    assert settings.cookie_samesite == "none"


def test_missing_settings_file_does_not_fall_back_to_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_settings_files(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PVP_SERVICE_NAME", raising=False)
    monkeypatch.delenv("PVP_COOKIE_SAMESITE", raising=False)
    monkeypatch.setenv("PVP_SETTINGS_FILE", ".env.missing")
    settings = load_settings()
    assert settings.service_name == "projektveckor-portal"
    assert settings.cookie_samesite == "lax"


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


def _scripts() -> dict[str, object]:
    parsed = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    scripts = parsed["tool"]["pdm"]["scripts"]
    assert isinstance(scripts, dict)
    return scripts


def _argv(script: object) -> list[str]:
    assert isinstance(script, str)
    return shlex.split(script)


WRAPPER = ["agent-secrets", "run", "--set", "projektveckor-portal-prod", "--"]


def test_serve_runs_uvicorn_through_the_wrapper_and_serve_lan_does_not() -> None:
    scripts = _scripts()
    serve = _argv(scripts["serve"])
    assert serve[: len(WRAPPER)] == WRAPPER
    assert serve[len(WRAPPER) : len(WRAPPER) + 2] == ["uvicorn", "projektveckor_portal.app:app"]
    assert "agent-secrets" not in _argv(scripts["serve:lan"])


def test_prod_compose_wraps_docker_compose_with_base_then_overlay() -> None:
    argv = _argv(_scripts()["prod-compose"])
    assert argv[: len(WRAPPER)] == WRAPPER
    rest = argv[len(WRAPPER) :]
    assert rest[:2] == ["docker", "compose"]
    assert rest[2:] == ["-f", "compose.prod.yaml", "-f", "compose.secrets.prod.yaml"]


@pytest.mark.parametrize("name", ["dev", "dev:lan"])
def test_dev_scripts_select_the_dev_settings_file(name: str) -> None:
    script = _scripts()[name]
    assert isinstance(script, dict)
    assert script["env"] == {"PVP_SETTINGS_FILE": ".env.dev"}
    argv = _argv(script["cmd"])
    assert argv[:2] == ["uvicorn", "projektveckor_portal.app:app"]
    assert "agent-secrets" not in argv


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


def _web_environment(compose: dict[str, object]) -> object:
    return _web_service(compose).get("environment")


def test_compose_files_deliver_the_key_only_through_the_overlay_web_environment() -> None:
    base = _load_yaml("compose.prod.yaml")
    overlay = _load_yaml("compose.secrets.prod.yaml")

    assert _key_locations(base) == []
    assert _key_locations(overlay) == [f"/services/web/environment/{KEY_NAME}"]
    assert "env_file" not in _web_service(base)
    assert "env_file" not in _web_service(overlay)
    assert ":?" not in json.dumps(base)
    overlay_environment = _web_environment(overlay)
    assert isinstance(overlay_environment, dict)
    assert overlay_environment[KEY_NAME] == f"${{{KEY_NAME}:?run through pdm run prod-compose}}"


def test_base_web_names_every_setting_as_a_value_less_or_fixed_entry() -> None:
    environment = _web_environment(_load_yaml("compose.prod.yaml"))
    assert isinstance(environment, dict)
    for field in Settings.model_fields:
        assert f"PVP_{field.upper()}" in environment, field
    for field in Settings.model_fields:
        value = environment[f"PVP_{field.upper()}"]
        assert value is None or field in {"environment", "service_version"}, field
