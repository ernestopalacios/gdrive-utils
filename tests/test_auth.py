"""Tests for gdrive_utils.auth.

These tests verify the authentication layer without making real Google calls.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gdrive_utils.auth import authorize
from gdrive_utils.config import GDriveConfig
from gdrive_utils.exceptions import AuthenticationError


class TestAuthorize:
    """authorise() behaviour."""

    def test_missing_credentials_file(self) -> None:
        cfg = GDriveConfig(credentials_path="/nonexistent/file.json")
        with pytest.raises(AuthenticationError, match="Credentials file not found"):
            authorize(cfg)

    @patch("gdrive_utils.auth.Credentials.from_service_account_file")
    @patch("gdrive_utils.auth.gspread.authorize")
    def test_successful_auth(
        self,
        mock_gspread_authorize: MagicMock,
        mock_from_file: MagicMock,
        tmp_path: Path,
    ) -> None:
        dummy_json = tmp_path / "dummy.json"
        dummy_json.write_text("{}")

        mock_creds = MagicMock()
        mock_from_file.return_value = mock_creds
        mock_client = MagicMock()
        mock_gspread_authorize.return_value = mock_client

        cfg = GDriveConfig(credentials_path=str(dummy_json))
        client = authorize(cfg)

        assert client is mock_client
        mock_from_file.assert_called_once_with(str(dummy_json), scopes=cfg.scope)
        mock_gspread_authorize.assert_called_once_with(mock_creds)

    @patch("gdrive_utils.auth.Credentials.from_service_account_file")
    def test_google_auth_error(
        self,
        mock_from_file: MagicMock,
        tmp_path: Path,
    ) -> None:
        from google.auth.exceptions import GoogleAuthError

        dummy_json = tmp_path / "dummy.json"
        dummy_json.write_text("{}")
        mock_from_file.side_effect = GoogleAuthError("bad credentials")

        cfg = GDriveConfig(credentials_path=str(dummy_json))
        with pytest.raises(AuthenticationError, match="Authentication failed"):
            authorize(cfg)
