# gdrive-utils

A reusable Python library for Google Drive/Sheets operations and file-renaming workflows.

## What is it?

`gdrive-utils` was extracted from the original `organizar.py` script so it can be shared across multiple projects via `uv add` or `pip install`.

The library provides two APIs:

- **Modern API** (recommended for new projects) — typed functions that raise custom exceptions and accept a [`GDriveConfig`](api/config.md) object.
- **Compatible API** (drop-in replacement) — the original function names and string-based error returns so existing code keeps working.

## Installation

```bash
uv add git+https://github.com/your-org/gdrive-utils.git
```

Or with pip:

```bash
pip install git+https://github.com/your-org/gdrive-utils.git
```

## Quick example

```python
from gdrive_utils import GDriveConfig, read_worksheet, build_filename

config = GDriveConfig(
    credentials_path="secrets/gdrive_credentials.json",
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
print(filename)  # OT [10] Cuadrilla 1 2024-01-15 (1) GJ.pdf
```

See the [User Guide](quickstart.md) for more details.
