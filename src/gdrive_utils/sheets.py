"""Google Sheets reading utilities (modern API)."""

import logging

import gspread
import pandas as pd

from .auth import authorize
from .config import GDriveConfig
from .exceptions import (
    AuthenticationError,
    DataFrameError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)

logger = logging.getLogger(__name__)


def read_worksheet(config: GDriveConfig | None = None) -> pd.DataFrame:
    """Open the configured spreadsheet/worksheet and return a DataFrame.

    Args:
        config: A :class:`GDriveConfig` instance. If ``None``, default
            configuration is used.

    Returns:
        A :class:`pandas.DataFrame` with the worksheet contents.

    Raises:
        AuthenticationError: If Google authentication fails.
        SpreadsheetNotFoundError: If the spreadsheet cannot be found.
        WorksheetNotFoundError: If the worksheet cannot be found.
        DataFrameError: If the worksheet is empty or data cannot be read.

    """
    if config is None:
        config = GDriveConfig()

    try:
        client = authorize(config)
    except AuthenticationError:
        raise

    try:
        sheet = client.open(config.spreadsheet_name)
        logger.info(
            "Successfully opened spreadsheet: '%s'", config.spreadsheet_name
        )
    except gspread.SpreadsheetNotFound as exc:
        logger.error(
            "Spreadsheet '%s' not found. Ensure it is shared with the service account.",
            config.spreadsheet_name,
        )
        raise SpreadsheetNotFoundError(
            f"Spreadsheet '{config.spreadsheet_name}' not found"
        ) from exc

    try:
        worksheet = sheet.worksheet(config.worksheet_name)
        logger.info("Selected worksheet: '%s'", worksheet.title)
    except gspread.WorksheetNotFound as exc:
        logger.error(
            "Worksheet '%s' not found in spreadsheet '%s'",
            config.worksheet_name,
            config.spreadsheet_name,
        )
        raise WorksheetNotFoundError(
            f"Worksheet '{config.worksheet_name}' not found"
        ) from exc

    try:
        data = worksheet.get_all_values()
    except gspread.GSpreadException as exc:
        logger.error("Error reading worksheet data: %s", exc)
        raise DataFrameError(f"Error reading worksheet data: {exc}") from exc

    if not data:
        logger.warning("The selected worksheet appears to be empty.")
        raise DataFrameError("Worksheet is empty")

    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)
    logger.info("Data successfully imported into DataFrame")

    # Drop rows with empty NOMBRE values (matches original logic)
    if "NOMBRE" in df.columns:
        df.loc[df["NOMBRE"] == "", "NOMBRE"] = pd.NA
        df = df.dropna(subset=["NOMBRE"])

    return df
