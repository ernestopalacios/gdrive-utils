"""Custom exception hierarchy for gdrive-utils."""


class GDriveUtilsError(Exception):
    """Base exception for all gdrive-utils errors."""

    pass


class AuthenticationError(GDriveUtilsError):
    """Raised when Google authentication fails."""

    pass


class SpreadsheetNotFoundError(GDriveUtilsError):
    """Raised when the specified spreadsheet cannot be found or accessed."""

    pass


class WorksheetNotFoundError(GDriveUtilsError):
    """Raised when the specified worksheet cannot be found in the spreadsheet."""

    pass


class DataFrameError(GDriveUtilsError):
    """Raised when a DataFrame operation fails or data is missing/invalid."""

    pass


class FileOperationError(GDriveUtilsError):
    """Raised when a file operation (move, rename, etc.) fails."""

    pass
