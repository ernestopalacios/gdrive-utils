"""Tests for gdrive_utils.compat.

These verify that the backward-compatible wrappers keep the original
behaviour (string error codes, same signatures, etc.).
"""

from unittest.mock import MagicMock

import pandas as pd

from gdrive_utils.compat import (
    from_name_get_cuadrilla,
    get_iniciales,
    get_nombre_archivo,
    get_nombre_corto_cuadrilla,
    get_num_cuadrilla,
    get_num_responsable,
    renombrar_ot,
)


class TestCompatWrappers:
    """Quick sanity checks for the old API surface."""

    def test_get_num_responsable_found(self, sample_df: pd.DataFrame) -> None:
        assert get_num_responsable("Juan Perez Garcia", sample_df) == "1"

    def test_get_num_responsable_not_df(self) -> None:
        assert get_num_responsable("X", "bad") == "x"

    def test_get_num_cuadrilla_found(self, sample_df: pd.DataFrame) -> None:
        assert get_num_cuadrilla("Z1 Cuadrilla A", sample_df) == "10"

    def test_get_num_cuadrilla_not_df(self) -> None:
        assert get_num_cuadrilla("X", "bad") == "XX"

    def test_get_iniciales_from_df(self, sample_df: pd.DataFrame) -> None:
        assert get_iniciales("Juan Perez Garcia", sample_df) == "GJ"

    def test_get_iniciales_vacio(self) -> None:
        assert get_iniciales("Ana Beatriz Castro") == "CA"

    def test_get_iniciales_short_name(self) -> None:
        assert get_iniciales("Ana Beatriz") == "revisar_nombre"

    def test_from_name_get_cuadrilla_found(self, sample_df: pd.DataFrame) -> None:
        assert from_name_get_cuadrilla("Juan Perez Garcia", sample_df) == "Z1 Cuadrilla A"

    def test_from_name_get_cuadrilla_not_df(self) -> None:
        assert from_name_get_cuadrilla("X", "bad") == "no"

    def test_get_nombre_corto_cuadrilla_from_df(self, sample_df: pd.DataFrame) -> None:
        assert get_nombre_corto_cuadrilla("Z1 Cuadrilla A", sample_df) == "Cuadrilla 1"

    def test_get_nombre_corto_cuadrilla_vacio(self) -> None:
        # Calculation path needs " Z" in the string
        assert get_nombre_corto_cuadrilla("Z5 ZCuadrilla X") == "Cuadrilla Z5"

    def test_get_nombre_archivo_valid(self, sample_df: pd.DataFrame) -> None:
        obj = MagicMock()
        obj.valido = True
        obj.data = {
            "cuadrilla": "Z1 Cuadrilla A",
            "responsable": ["Juan Perez Garcia"],
            "fecha": "2024-01-15T10:30:00",
        }
        obj.link = "https://example.com/file.pdf"
        obj.Log2Ot = MagicMock()

        result = get_nombre_archivo(obj, sample_df)
        assert result == "OT [10] Cuadrilla 1 2024-01-15 (1) GJ.pdf"
        obj.Log2Ot.assert_not_called()

    def test_get_nombre_archivo_invalid(self, sample_df: pd.DataFrame) -> None:
        obj = MagicMock()
        obj.valido = False
        obj.link = "https://example.com/original.pdf"
        obj.Log2Ot = MagicMock()

        result = get_nombre_archivo(obj, sample_df)
        assert result == "original.pdf"
        obj.Log2Ot.assert_not_called()

    def test_get_nombre_archivo_error(self, sample_df: pd.DataFrame) -> None:
        obj = MagicMock()
        obj.valido = True
        obj.data = {}  # missing keys -> exception
        obj.link = "https://example.com/fallback.pdf"
        obj.Log2Ot = MagicMock()

        result = get_nombre_archivo(obj, sample_df)
        assert result == "fallback.pdf"
        obj.Log2Ot.assert_called_once()

    def test_renombrar_ot_success(self, tmp_path) -> None:
        src = tmp_path / "a.txt"
        src.write_text("x")
        result = renombrar_ot(str(src), "b.txt")
        assert result.endswith("ot_procesados/b.txt")

    def test_renombrar_ot_failure(self, tmp_path) -> None:
        result = renombrar_ot(str(tmp_path / "missing.txt"), "x.txt")
        assert result == "Failed"
