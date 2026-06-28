# Quick Start

## Modern API (recommended)

Import the typed functions and create a [`GDriveConfig`](api/config.md):

```python
from gdrive_utils import GDriveConfig, read_worksheet, build_filename, move_file

# Configuration is read from env var GDRIVE_CREDENTIALS_PATH or uses defaults.
config = GDriveConfig(
    spreadsheet_name="DB_calificar_ot",
    worksheet_name="Iniciales",
)

df = read_worksheet(config)

data = {
    "cuadrilla": "Z1 Cuadrilla A",
    "responsable": ["Juan Perez Garcia"],
    "fecha": "2024-01-15T10:30:00",
}
filename = build_filename(data, df)
new_path = move_file("/path/to/old.pdf", filename)
```

### Error handling

The modern API raises typed exceptions:

| Exception | When it happens |
|---|---|
| `AuthenticationError` | Credentials file missing or invalid |
| `SpreadsheetNotFoundError` | Google Sheet not found or not shared |
| `WorksheetNotFoundError` | Worksheet tab does not exist |
| `DataFrameError` | Required columns missing or sheet empty |
| `FileOperationError` | File move/rename fails |

```python
from gdrive_utils import (
    read_worksheet,
    AuthenticationError,
    SpreadsheetNotFoundError,
)

try:
    df = read_worksheet()
except AuthenticationError:
    print("Check your credentials file")
except SpreadsheetNotFoundError:
    print("Make sure the sheet is shared with the service account")
```

## Compatible API (drop-in)

If you already have code using the original `organizar.py` functions, simply change the import:

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

All function names, signatures, and string error returns remain identical.

## Next steps

- Read about [Configuration](configuration.md)
- Browse the [API Reference](api.md)
