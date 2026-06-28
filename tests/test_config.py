"""Tests for gdrive_utils.config."""


import pytest

from gdrive_utils.config import GDriveConfig


class TestGDriveConfig:
    """GDriveConfig dataclass behaviour."""

    def test_default_values(self) -> None:
        cfg = GDriveConfig()
        assert cfg.spreadsheet_name == "DB_calificar_ot"
        assert cfg.worksheet_name == "Iniciales"
        assert "spreadsheets" in cfg.scope[0]
        assert "drive" in cfg.scope[1]

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GDRIVE_CREDENTIALS_PATH", "/tmp/fake.json")
        cfg = GDriveConfig()
        assert cfg.credentials_path == "/tmp/fake.json"

    def test_explicit_path_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GDRIVE_CREDENTIALS_PATH", "/tmp/fake.json")
        cfg = GDriveConfig(credentials_path="/tmp/other.json")
        assert cfg.credentials_path == "/tmp/other.json"
