"""Core data-processing functions (modern API).

These functions accept plain DataFrames and raise custom exceptions on errors.
"""

import logging

import pandas as pd

from .exceptions import DataFrameError

logger = logging.getLogger(__name__)


def get_responsable_order(name: str, df: pd.DataFrame) -> str:
    """Return the *ORDEN_RESPONSABLE* value for *name*.

    Args:
        name: The person's full name.
        df: The personnel DataFrame.

    Returns:
        The order string, or ``'0'`` if the name is not found.

    Raises:
        DataFrameError: If *df* is not a DataFrame or required columns are missing.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")
    if "NOMBRE" not in df.columns or "ORDEN_RESPONSABLE" not in df.columns:
        raise DataFrameError("Required columns missing: NOMBRE, ORDEN_RESPONSABLE")

    series = df.query(f"NOMBRE == {name!r}")["ORDEN_RESPONSABLE"]
    if not series.empty:
        return str(series.iloc[0])
    return "0"


def get_cuadrilla_order(cuadrilla_ot: str, df: pd.DataFrame) -> str:
    """Return the *ORDEN_CUADRILLA* value for *cuadrilla_ot*.

    Args:
        cuadrilla_ot: The cuadrilla identifier.
        df: The personnel DataFrame.

    Returns:
        The order string, or ``'no'`` if not found.

    Raises:
        DataFrameError: If *df* is not a DataFrame or required columns are missing.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")
    if "CUADRILLA_OT" not in df.columns or "ORDEN_CUADRILLA" not in df.columns:
        raise DataFrameError("Required columns missing: CUADRILLA_OT, ORDEN_CUADRILLA")

    series = df.query(f"CUADRILLA_OT == {cuadrilla_ot!r}")["ORDEN_CUADRILLA"]
    if not series.empty:
        return str(series.iloc[0])
    return "no"


def get_initials(name: str, df: pd.DataFrame) -> str:
    """Return initials for *name*.

    If *df* contains an *INICIALES* column and the name is found there, the
    stored value is returned. Otherwise initials are calculated from the name
    itself, with a collision check against the DataFrame.

    Args:
        name: The person's full name (at least three parts recommended).
        df: The personnel DataFrame.

    Returns:
        The initials string.

    Raises:
        DataFrameError: If *df* is not a DataFrame.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")

    df_has_initials = (
        "NOMBRE" in df.columns and "INICIALES" in df.columns
    )

    if df_has_initials:
        series = df.query(f"NOMBRE == {name!r}")["INICIALES"]
        if not series.empty:
            return str(series.iloc[0])

    name_parts = name.split(" ")
    if len(name_parts) < 3:
        return "revisar_nombre"

    calculated = name_parts[2][0] + name_parts[0][0]

    if not df_has_initials:
        return calculated

    # Collision check
    check = df.query(f"INICIALES == {calculated!r}")["NOMBRE"]
    if check.empty:
        return calculated

    # Append second name initial to disambiguate
    return calculated + name_parts[1][0]


def get_cuadrilla_by_name(name: str, df: pd.DataFrame) -> str:
    """Return the *CUADRILLA_OT* value associated with *name*.

    Args:
        name: The person's full name.
        df: The personnel DataFrame.

    Returns:
        The cuadrilla string, or ``'no'`` if not found.

    Raises:
        DataFrameError: If *df* is not a DataFrame or required columns are missing.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")
    if "NOMBRE" not in df.columns or "CUADRILLA_OT" not in df.columns:
        raise DataFrameError("Required columns missing: NOMBRE, CUADRILLA_OT")

    series = df.query(f"NOMBRE == {name!r}")["CUADRILLA_OT"]
    if not series.empty:
        return str(series.iloc[0])
    return "no"


def get_short_cuadrilla_name(cuadrilla: str, df: pd.DataFrame) -> str:
    """Return a short display name for *cuadrilla*.

    If *df* contains a *CUADRILLA_CORTO* column and the cuadrilla is found
    there, the stored short name is returned. Otherwise a short name is
    calculated from the cuadrilla string.

    Args:
        cuadrilla: The full cuadrilla name.
        df: The personnel DataFrame.

    Returns:
        The short cuadrilla name.

    Raises:
        DataFrameError: If *df* is not a DataFrame.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")

    if "CUADRILLA_OT" in df.columns and "CUADRILLA_CORTO" in df.columns:
        series = df.query(f"CUADRILLA_OT == {cuadrilla!r}")["CUADRILLA_CORTO"]
        if not series.empty:
            return str(series.iloc[0])

    try:
        grupo, tipo = cuadrilla.split(" Z")
    except ValueError:
        return cuadrilla

    if "Cuadrilla" in tipo:
        return f"Cuadrilla {grupo}"
    if "Agencia" in tipo:
        return f"Agencia {grupo}"

    return cuadrilla


def get_all_data(value: str, column: str, df: pd.DataFrame) -> dict:
    """Return **all** columns for the first row where *column* equals *value*.

    Every column present in the DataFrame is included in the result
    dynamically — no hardcoded field list.  All values are returned as
    strings, except ``USER_ID`` which is converted to an ``int``.

    Args:
        value: The value to look up.
        column: The DataFrame column to search in.
        df: The personnel DataFrame.

    Returns:
        A dictionary with keys for every column in *df*.

    Raises:
        DataFrameError: If *df* is not a DataFrame, *column* does not exist,
            or no matching row is found.

    """
    if not isinstance(df, pd.DataFrame):
        raise DataFrameError("Expected a pandas DataFrame")
    if column not in df.columns:
        raise DataFrameError(f"Column '{column}' not found in DataFrame")

    mask = df[column] == value
    matches = df[mask]

    if matches.empty:
        raise DataFrameError(
            f"No match found for '{value}' in column '{column}'"
        )

    if len(matches) > 1:
        logger.warning(
            "Multiple matches (%d) for '%s' in '%s'; returning first row",
            len(matches),
            value,
            column,
        )

    row = matches.iloc[0]
    result: dict = {}
    for col in df.columns:
        val = row[col]
        if col == "USER_ID":
            try:
                result[col] = int(val)
            except (ValueError, TypeError) as exc:
                raise DataFrameError(
                    f"USER_ID value '{val}' cannot be converted to int"
                ) from exc
        else:
            result[col] = str(val)

    return result


def build_filename(data: dict, df: pd.DataFrame) -> str:
    """Build a standardised filename from *data* and personnel *df*.

    Args:
        data: A dictionary with keys ``cuadrilla``, ``responsable`` (list),
            and ``fecha``.
        df: The personnel DataFrame.

    Returns:
        The generated filename.

    Raises:
        DataFrameError: If required DataFrame columns are missing.
        KeyError: If required keys are missing from *data*.

    """
    cuadrilla = data["cuadrilla"]
    responsable_name = data["responsable"][0]
    fecha_raw = data["fecha"]

    num_cuadrilla = get_cuadrilla_order(cuadrilla, df)
    num_responsable = get_responsable_order(responsable_name, df)
    iniciales = get_initials(responsable_name, df)
    cuadrilla_corto = get_short_cuadrilla_name(cuadrilla, df)

    try:
        fecha = fecha_raw.split("T")[0]
    except (AttributeError, IndexError):
        fecha = str(fecha_raw)

    return (
        f"OT [{num_cuadrilla}] {cuadrilla_corto} {fecha} "
        f"({num_responsable}) {iniciales}.pdf"
    )
