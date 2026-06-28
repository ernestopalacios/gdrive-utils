"""Shared fixtures and helpers for the test suite."""

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Return a minimal DataFrame that mimics the real personnel sheet."""
    return pd.DataFrame(
        {
            "NOMBRE": [
                "Juan Perez Garcia",
                "Maria Lopez Torres",
                "Carlos Ruiz Diaz",
            ],
            "INICIALES": ["GJ", "TM", "DC"],
            "ORDEN_RESPONSABLE": ["1", "2", "3"],
            "CUADRILLA_OT": [
                "Z1 Cuadrilla A",
                "Z2 Agencia B",
                "Z3 Especial",
            ],
            "ORDEN_CUADRILLA": ["10", "20", "30"],
            "CUADRILLA_CORTO": ["Cuadrilla 1", "Agencia 2", "Especial 3"],
        }
    )


@pytest.fixture
def empty_df() -> pd.DataFrame:
    """Return an empty DataFrame with the expected columns."""
    return pd.DataFrame(
        columns=[
            "NOMBRE",
            "INICIALES",
            "ORDEN_RESPONSABLE",
            "CUADRILLA_OT",
            "ORDEN_CUADRILLA",
            "CUADRILLA_CORTO",
        ]
    )
