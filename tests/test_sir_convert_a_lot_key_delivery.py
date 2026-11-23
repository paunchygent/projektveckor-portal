from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
import yaml

from projektveckor_portal.settings import Settings

REPO_ROOT = Path(__file__).resolve().parents[1]

_SIR_ENV_NAMES = [
    "SIR_CONVERT_A_LOT_V2_API_KEY",
    "PVP_SIR_CONVERT_A_LOT_API_KEY",
    "PVP_SIR_CONVERT_A_LOT_V2_API_KEY",
    "SIR_CONVERT_A_LOT_API_KEY",
]


@pytest.fixture(autouse=True)
def _clean_sir_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _SIR_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def _pdm_scripts() -> dict[str, object]:
    parsed = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    scripts: dict[str, object] = parsed["tool"]["pdm"]["scripts"]
    return scripts


def test_settings_reads_canonical_sir_key_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SIR_CONVERT_A_LOT_V2_API_KEY", "test-key")
    assert Settings().sir_convert_a_lot_api_key == "test-key"


def test_settings_ignores_legacy_sir_key_names(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _SIR_ENV_NAMES[1:]:
        monkeypatch.setenv(name, "test-key")
    assert Settings().sir_convert_a_lot_api_key is None


def test_settings_does_not_read_sir_key_from_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / ".env").write_text("SIR_CONVERT_A_LOT_V2_API_KEY=test-key\n")
    monkeypatch.chdir(tmp_path)
    assert Settings().sir_convert_a_lot_api_key is None


def test_prod_compose_runs_compose_through_agent_secrets() -> None:
    command = _pdm_scripts()["prod-compose"]
    assert isinstance(command, str)
    assert command.startswith("agent-secrets run --set projektveckor-portal-prod -- docker compose")
    assert command.index("-f compose.prod.yaml") < command.index("-f compose.secrets.prod.yaml")


def test_dev_scripts_load_dev_env_file() -> None:
    scripts = _pdm_scripts()
    for name in ("dev", "dev:lan"):
        script = scripts[name]
        assert isinstance(script, dict)
        assert script["env_file"] == ".env.dev"


def test_prod_compose_files_keep_secrets_in_the_overlay() -> None:
    base_text = (REPO_ROOT / "compose.prod.yaml").read_text()
    assert "SIR_CONVERT_A_LOT_V2_API_KEY" not in base_text
    base = yaml.safe_load(base_text)
    assert "env_file" not in base["services"]["web"]

    overlay_text = (REPO_ROOT / "compose.secrets.prod.yaml").read_text()
    assert "PVP_SIR_CONVERT_A_LOT_API_KEY" not in overlay_text
    assert "${SIR_CONVERT_A_LOT_V2_API_KEY:?" in overlay_text
