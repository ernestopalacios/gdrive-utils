"""Tests for gdrive_utils.core."""

import pandas as pd
import pytest

from gdrive_utils.core import (
    build_filename,
    get_all_data,
    get_cuadrilla_by_name,
    get_cuadrilla_order,
    get_initials,
    get_responsable_order,
    get_short_cuadrilla_name,
)
from gdrive_utils.exceptions import DataFrameError


class TestGetResponsableOrder:
    def test_found(self, sample_df: pd.DataFrame) -> None:
        assert get_responsable_order("Juan Perez Garcia", sample_df) == "1"

    def test_not_found(self, sample_df: pd.DataFrame) -> None:
        assert get_responsable_order("Missing Name", sample_df) == "0"

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_responsable_order("X", "not a df")  # type: ignore[arg-type]

    def test_missing_columns(self) -> None:
        bad_df = pd.DataFrame({"A": [1]})
        with pytest.raises(DataFrameError):
            get_responsable_order("X", bad_df)


class TestGetCuadrillaOrder:
    def test_found(self, sample_df: pd.DataFrame) -> None:
        assert get_cuadrilla_order("Z1 Cuadrilla A", sample_df) == "10"

    def test_not_found(self, sample_df: pd.DataFrame) -> None:
        assert get_cuadrilla_order("Unknown", sample_df) == "no"

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_cuadrilla_order("X", "not a df")  # type: ignore[arg-type]


class TestGetInitials:
    def test_from_dataframe(self, sample_df: pd.DataFrame) -> None:
        assert get_initials("Juan Perez Garcia", sample_df) == "GJ"

    def test_calculated_no_collision(self, sample_df: pd.DataFrame) -> None:
        # This name is not in the df, so initials are calculated
        result = get_initials("Ana Beatriz Castro", sample_df)
        assert result == "CA"  # Castro[0] + Ana[0]

    def test_calculated_with_collision(self, sample_df: pd.DataFrame) -> None:
        # Force a collision: "Juan Perez Garcia" already has "GJ"
        # Use a different name that would also compute to "GJ"
        result = get_initials("Juan Pablo Garcia", sample_df)
        assert result == "GJP"  # Garcia + Juan + Pablo (collision adds middle)

    def test_short_name(self) -> None:
        df = pd.DataFrame()
        assert get_initials("Ana Beatriz", df) == "revisar_nombre"

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_initials("X", "not a df")  # type: ignore[arg-type]


class TestGetCuadrillaByName:
    def test_found(self, sample_df: pd.DataFrame) -> None:
        assert get_cuadrilla_by_name("Juan Perez Garcia", sample_df) == "Z1 Cuadrilla A"

    def test_not_found(self, sample_df: pd.DataFrame) -> None:
        assert get_cuadrilla_by_name("Missing", sample_df) == "no"

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_cuadrilla_by_name("X", "not a df")  # type: ignore[arg-type]


class TestGetShortCuadrillaName:
    def test_from_dataframe(self, sample_df: pd.DataFrame) -> None:
        assert get_short_cuadrilla_name("Z1 Cuadrilla A", sample_df) == "Cuadrilla 1"

    def test_calculated_cuadrilla(self, sample_df: pd.DataFrame) -> None:
        # String contains " Z" so the split-based calculation triggers
        assert get_short_cuadrilla_name("Z5 ZCuadrilla X", sample_df) == "Cuadrilla Z5"

    def test_calculated_agencia(self, sample_df: pd.DataFrame) -> None:
        assert get_short_cuadrilla_name("Z9 ZAgencia Y", sample_df) == "Agencia Z9"

    def test_special_name(self, sample_df: pd.DataFrame) -> None:
        # Not in df, split works but type is neither Cuadrilla nor Agencia
        assert get_short_cuadrilla_name("Z7 ZEspecial", sample_df) == "Z7 ZEspecial"

    def test_no_z_prefix(self, sample_df: pd.DataFrame) -> None:
        assert get_short_cuadrilla_name("Random", sample_df) == "Random"

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_short_cuadrilla_name("X", "not a df")  # type: ignore[arg-type]


class TestGetAllData:
    def test_by_name(self, sample_df: pd.DataFrame) -> None:
        result = get_all_data("Juan Perez Garcia", "NOMBRE", sample_df)
        assert result["NOMBRE"] == "Juan Perez Garcia"
        assert result["INICIALES"] == "GJ"
        assert result["ORDEN_RESPONSABLE"] == "1"
        assert result["CUADRILLA_OT"] == "Z1 Cuadrilla A"
        assert result["CUADRILLA_CORTO"] == "Cuadrilla 1"
        assert result["ORDEN_CUADRILLA"] == "10"
        assert result["USER_ID"] == 1001

    def test_by_initials(self, sample_df: pd.DataFrame) -> None:
        result = get_all_data("TM", "INICIALES", sample_df)
        assert result["NOMBRE"] == "Maria Lopez Torres"
        assert result["USER_ID"] == 1002

    def test_by_cuadrilla_ot(self, sample_df: pd.DataFrame) -> None:
        result = get_all_data("Z3 Especial", "CUADRILLA_OT", sample_df)
        assert result["NOMBRE"] == "Carlos Ruiz Diaz"
        assert result["ORDEN_CUADRILLA"] == "30"
        assert result["USER_ID"] == 1003

    def test_no_match(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(DataFrameError, match="No match found"):
            get_all_data("NONEXISTENT", "NOMBRE", sample_df)

    def test_missing_column(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(DataFrameError, match="Column 'MISSING' not found"):
            get_all_data("X", "MISSING", sample_df)

    def test_bad_df(self) -> None:
        with pytest.raises(DataFrameError):
            get_all_data("X", "NOMBRE", "not a df")  # type: ignore[arg-type]

    def test_user_id_conversion_error(self, sample_df: pd.DataFrame) -> None:
        bad_df = sample_df.copy()
        bad_df["USER_ID"] = ["not_a_number", "1002", "1003"]
        with pytest.raises(DataFrameError, match="cannot be converted to int"):
            get_all_data("Juan Perez Garcia", "NOMBRE", bad_df)


class TestBuildFilename:
    def test_success(self, sample_df: pd.DataFrame) -> None:
        data = {
            "cuadrilla": "Z1 Cuadrilla A",
            "responsable": ["Juan Perez Garcia"],
            "fecha": "2024-01-15T10:30:00",
        }
        result = build_filename(data, sample_df)
        assert result == "OT [10] Cuadrilla 1 2024-01-15 (1) GJ.pdf"

    def test_date_without_t(self, sample_df: pd.DataFrame) -> None:
        data = {
            "cuadrilla": "Z1 Cuadrilla A",
            "responsable": ["Juan Perez Garcia"],
            "fecha": "2024-06-01",
        }
        result = build_filename(data, sample_df)
        assert result == "OT [10] Cuadrilla 1 2024-06-01 (1) GJ.pdf"

    def test_missing_key(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            build_filename({}, sample_df)
