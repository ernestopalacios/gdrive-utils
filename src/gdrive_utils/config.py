"""Configuration dataclass for gdrive-utils."""

import os
from dataclasses import dataclass, field


@dataclass
class GDriveConfig:
    """Configuration for Google Drive/Sheets operations.

    The *credentials_path* defaults to the value of the environment variable
    ``GDRIVE_CREDENTIALS_PATH`` (if set), otherwise falls back to
    ``secrets/gdrive_credentials.json``.
    """

    credentials_path: str = field(
        default_factory=lambda: os.getenv(
            "GDRIVE_CREDENTIALS_PATH", "secrets/gdrive_credentials.json"
        )
    )
    spreadsheet_name: str = "DB_calificar_ot"
    worksheet_name: str = "Iniciales"
    scope: list[str] = field(
        default_factory=lambda: [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
    )
