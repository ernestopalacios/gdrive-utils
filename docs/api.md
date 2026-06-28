# API Reference

The library is organised into several modules:

| Module | Purpose |
|---|---|
| [`gdrive_utils.exceptions`](api/exceptions.md) | Custom exception hierarchy |
| [`gdrive_utils.config`](api/config.md) | Configuration dataclass |
| [`gdrive_utils.auth`](api/auth.md) | Google authentication |
| [`gdrive_utils.sheets`](api/sheets.md) | Google Sheets reading |
| [`gdrive_utils.core`](api/core.md) | Data-processing functions |
| [`gdrive_utils.files`](api/files.md) | File operations |
| [`gdrive_utils.compat`](api/compat.md) | Backward-compatible wrappers |

## Modern API overview

```python
from gdrive_utils import (
    GDriveConfig,
    read_worksheet,
    get_responsable_order,
    get_cuadrilla_order,
    get_initials,
    get_cuadrilla_by_name,
    get_short_cuadrilla_name,
    build_filename,
    move_file,
)
```

## Compatible API overview

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

See the individual module pages for full API details.
