# gdrive-utils

A reusable Python library for Google Drive/Sheets operations and file-renaming workflows. Extracted from the original `organizar.py` script so it can be shared across multiple projects via `uv add` or `pip install`.

## Installation

```bash
uv add git+https://github.com/ernestopalacios/gdrive-utils.git
```

Or with pip:

```bash
pip install git+https://github.com/ernestopalacios/gdrive-utils.git
```

## Quick start

### Modern API (recommended for new projects)

```python
from gdrive_utils import GDriveConfig, read_worksheet, build_filename

# Optional: override defaults via env var GDRIVE_CREDENTIALS_PATH
config = GDriveConfig(
    credentials_path="secrets/gdrive_credentials.json",
    spreadsheet_name="DB_calificar_ot",
    worksheet_name="Iniciales",
)

df = read_worksheet(config)

# Build a filename from plain data
data = {
    "cuadrilla": "Z1 Cuadrilla A",
    "responsable": ["Juan Perez Garcia"],
    "fecha": "2024-01-15T10:30:00",
}
filename = build_filename(data, df)
print(filename)  # -> OT [10] Cuadrilla 1 2024-01-15 (1) GJ.pdf
```

### Compatible API (drop-in replacement for *organizar.py*)

If you already have code that imports from the old script, simply change the import:

```python
from gdrive_utils import (
    get_gsheet_df,
    get_num_responsable,
    get_num_cuadrilla,
    get_iniciales,
    from_name_get_cuadrilla,
    get_nombre_corto_cuadrilla,
    get_nombre_archivo,
    renombrar_ot,
)
```

All function names, signatures, and error-string returns remain identical.

## Error handling

The modern API raises typed exceptions:

| Exception | Raised when … |
|---|---|
| `AuthenticationError` | Service-account credentials are missing or invalid |
| `SpreadsheetNotFoundError` | The Google Sheet cannot be found or accessed |
| `WorksheetNotFoundError` | The requested worksheet tab does not exist |
| `DataFrameError` | Required columns are missing or the sheet is empty |
| `FileOperationError` | A file move/rename fails |

The compatible API catches these internally and returns the original string codes (`"Fail"`, `"0"`, `"no"`, etc.).

## Configuration

`GDriveConfig` supports an environment variable fallback:

```bash
export GDRIVE_CREDENTIALS_PATH=/path/to/credentials.json
```

If the variable is not set, the default `secrets/gdrive_credentials.json` is used.

## Development

```bash
uv sync --group dev        # install + dev dependencies
uv run pytest -v            # run tests
uv run ruff check src tests # lint
uv run mypy src             # type check
```

## License

Add your license here.
