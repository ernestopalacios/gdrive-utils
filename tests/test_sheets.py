"""Tests for gdrive_utils.sheets.

We mock *gspread* interactions to avoid real Google API calls.
"""

from unittest.mock import MagicMock, patch

import gspread
import pandas as pd
import pytest

from gdrive_utils.config import GDriveConfig
from gdrive_utils.exceptions import (
    DataFrameError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)
from gdrive_utils.sheets import read_worksheet


class TestReadWorksheet:
    """read_worksheet() mocked scenarios."""

    @patch("gdrive_utils.sheets.authorize")
    def test_spreadsheet_not_found(self, mock_authorize: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.open.side_effect = gspread.SpreadsheetNotFound
        mock_authorize.return_value = mock_client

        with pytest.raises(SpreadsheetNotFoundError):
            read_worksheet(GDriveConfig())

    @patch("gdrive_utils.sheets.authorize")
    def test_worksheet_not_found(self, mock_authorize: MagicMock) -> None:
        mock_sheet = MagicMock()
        mock_sheet.worksheet.side_effect = gspread.WorksheetNotFound("missing")
        mock_client = MagicMock()
        mock_client.open.return_value = mock_sheet
        mock_authorize.return_value = mock_client

        with pytest.raises(WorksheetNotFoundError):
            read_worksheet(GDriveConfig())

    @patch("gdrive_utils.sheets.authorize")
    def test_empty_worksheet(self, mock_authorize: MagicMock) -> None:
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_values.return_value = []
        mock_sheet = MagicMock()
        mock_sheet.worksheet.return_value = mock_worksheet
        mock_client = MagicMock()
        mock_client.open.return_value = mock_sheet
        mock_authorize.return_value = mock_client

        with pytest.raises(DataFrameError, match="empty"):
            read_worksheet(GDriveConfig())

    @patch("gdrive_utils.sheets.authorize")
    def test_successful_read(self, mock_authorize: MagicMock) -> None:
        mock_worksheet = MagicMock()
        mock_worksheet.title = "Iniciales"
        mock_worksheet.get_all_values.return_value = [
            ["NOMBRE", "INICIALES"],
            ["Juan Perez Garcia", "GJ"],
            ["", ""],  # empty row to be dropped
        ]
        mock_sheet = MagicMock()
        mock_sheet.worksheet.return_value = mock_worksheet
        mock_client = MagicMock()
        mock_client.open.return_value = mock_sheet
        mock_authorize.return_value = mock_client

        df = read_worksheet(GDriveConfig())
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]["NOMBRE"] == "Juan Perez Garcia"
