"""gdrive-utils — Google Drive/Sheets utility library.

This package exposes two APIs:

* **Modern API** (recommended for new projects) — functions in
  :mod:`gdrive_utils.sheets`, :mod:`gdrive_utils.core`, and
  :mod:`gdrive_utils.files`. They raise custom exceptions and accept a
  :class:`gdrive_utils.config.GDriveConfig` object.

* **Compatible API** (drop-in replacement for *organizar.py*) — functions in
  :mod:`gdrive_utils.compat`. They keep the original names and return string
  error codes.

Public types
------------
"""

from .compat import (
    from_name_get_cuadrilla,
    get_gsheet_df,
    get_iniciales,
    get_nombre_archivo,
    get_nombre_corto_cuadrilla,
    get_num_cuadrilla,
    get_num_responsable,
    renombrar_ot,
)
from .config import GDriveConfig
from .core import (
    build_filename,
    get_all_data,
    get_cuadrilla_by_name,
    get_cuadrilla_order,
    get_initials,
    get_responsable_order,
    get_short_cuadrilla_name,
)
from .exceptions import (
    AuthenticationError,
    DataFrameError,
    FileOperationError,
    GDriveUtilsError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)
from .files import move_file
from .sheets import read_worksheet

__all__ = [
    # Config
    "GDriveConfig",
    # Exceptions
    "GDriveUtilsError",
    "AuthenticationError",
    "SpreadsheetNotFoundError",
    "WorksheetNotFoundError",
    "DataFrameError",
    "FileOperationError",
    # Modern API
    "read_worksheet",
    "get_responsable_order",
    "get_cuadrilla_order",
    "get_initials",
    "get_cuadrilla_by_name",
    "get_short_cuadrilla_name",
    "get_all_data",
    "build_filename",
    "move_file",
    # Compatible API
    "get_gsheet_df",
    "get_num_responsable",
    "get_num_cuadrilla",
    "get_iniciales",
    "from_name_get_cuadrilla",
    "get_nombre_corto_cuadrilla",
    "get_nombre_archivo",
    "renombrar_ot",
]
