"""Backward-compatible wrappers from the original *organizar.py*.

These keep the exact function names and string-based error returns.
New projects should use the modern API in :mod:`gdrive_utils.sheets`,
:mod:`gdrive_utils.core`, and :mod:`gdrive_utils.files` instead.
"""

import logging
import os
from typing import Any

import pandas as pd

from .config import GDriveConfig
from .core import (
    build_filename,
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
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)
from .files import move_file as _move_file
from .sheets import read_worksheet

logger = logging.getLogger(__name__)


def get_gsheet_df(df: pd.DataFrame | None = None) -> pd.DataFrame | str:
    """Original wrapper: returns a DataFrame or the string ``'Fail'``.

    Parameters are ignored for backward compatibility; the default
    :class:`GDriveConfig` is used.
    """
    try:
        return read_worksheet(GDriveConfig())
    except AuthenticationError:
        logger.info("Authentication failed")
        return "Fail"
    except SpreadsheetNotFoundError:
        logger.info(
            "Error: Spreadsheet not found. "
            "Make sure the name is correct and the sheet is shared with the service account email."
        )
        return "Fail"
    except WorksheetNotFoundError:
        logger.info("Error: Worksheet not found in the spreadsheet.")
        return "Fail"
    except DataFrameError:
        logger.info("Error: The selected worksheet appears to be empty.")
        return "Fail"
    except Exception as exc:
        logger.info("An error occurred while accessing the sheet/worksheet: %s", exc)
        return "Fail"


def get_num_responsable(nombre: str, df: pd.DataFrame | str) -> str:
    """Original wrapper: returns order string, ``'0'``, or ``'x'``."""
    if not isinstance(df, pd.DataFrame):
        return "x"
    try:
        return get_responsable_order(nombre, df)
    except DataFrameError as exc:
        logger.info("DataFrame error in get_num_responsable: %s", exc)
        return "x"


def get_num_cuadrilla(cuadrilla_ot: str, df: pd.DataFrame | str) -> str:
    """Original wrapper: returns order string, ``'no'``, or ``'XX'``."""
    if not isinstance(df, pd.DataFrame):
        return "XX"
    try:
        return get_cuadrilla_order(cuadrilla_ot, df)
    except DataFrameError as exc:
        logger.info("DataFrame error in get_num_cuadrilla: %s", exc)
        return "no"


def get_iniciales(nombre: str, df: pd.DataFrame | str = "vacio") -> str:
    """Original wrapper: returns initials or ``'revisar_nombre'``."""
    if isinstance(df, str) and df == "vacio":
        df = pd.DataFrame()  # empty DataFrame triggers calculation path
    if not isinstance(df, pd.DataFrame):
        return "revisar_nombre"
    try:
        return get_initials(nombre, df)
    except DataFrameError:
        return "revisar_nombre"


def from_name_get_cuadrilla(nombre: str, df: pd.DataFrame | str) -> str:
    """Original wrapper: returns cuadrilla name or ``'no'``."""
    if not isinstance(df, pd.DataFrame):
        return "no"
    try:
        return get_cuadrilla_by_name(nombre, df)
    except DataFrameError as exc:
        logger.info("DataFrame error in from_name_get_cuadrilla: %s", exc)
        return "no"


def get_nombre_corto_cuadrilla(cuadrilla: str, df: pd.DataFrame | str = "vacio") -> str:
    """Original wrapper: returns short name or the original string."""
    if isinstance(df, str) and df == "vacio":
        df = pd.DataFrame()
    if not isinstance(df, pd.DataFrame):
        return cuadrilla
    try:
        return get_short_cuadrilla_name(cuadrilla, df)
    except DataFrameError:
        return cuadrilla


def get_nombre_archivo(obj: Any, df: pd.DataFrame | str = "vacio") -> str:
    """Original wrapper that accepts the old *obj* interface.

    On any error calls ``obj.Log2Ot`` and returns ``os.path.basename(obj.link)``.
    """
    if isinstance(df, str) and df == "vacio":
        df = pd.DataFrame()
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()

    try:
        if not getattr(obj, "valido", True):
            return str(os.path.basename(obj.link))

        data = {
            "cuadrilla": obj.data["cuadrilla"],
            "responsable": obj.data["responsable"],
            "fecha": obj.data["fecha"],
        }
        return build_filename(data, df)
    except Exception as exc:
        logger.info("No fue posible renombrar la OT Error: %s", exc)
        obj.Log2Ot(
            "ERROR",
            "No fue posible renombrar la OT",
            "No se pudo extraer la información de la Orden de Trabajo para ser renombrada",
        )
        return str(os.path.basename(obj.link))


def renombrar_ot(current_file_path: str, nombre_nuevo: str) -> str:
    """Original wrapper: returns destination path or ``'Failed'``."""
    try:
        return _move_file(current_file_path, nombre_nuevo)
    except FileOperationError as exc:
        logger.info("Error moving/renaming file: %s", exc)
        return "Failed"
    except Exception as exc:
        logger.info("Error: %s", exc)
        return "Failed"
