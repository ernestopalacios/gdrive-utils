"""Tests for gdrive_utils.exceptions."""

import pytest

from gdrive_utils.exceptions import (
    AuthenticationError,
    DataFrameError,
    FileOperationError,
    GDriveUtilsError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)


class TestExceptionHierarchy:
    """Ensure every custom exception inherits from GDriveUtilsError."""

    @pytest.mark.parametrize(
        "exc_class",
        [
            AuthenticationError,
            SpreadsheetNotFoundError,
            WorksheetNotFoundError,
            DataFrameError,
            FileOperationError,
        ],
    )
    def test_inheritance(self, exc_class: type[Exception]) -> None:
        exc = exc_class("boom")
        assert isinstance(exc, GDriveUtilsError)
