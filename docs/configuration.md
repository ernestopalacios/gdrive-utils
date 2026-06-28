# Configuration

## `GDriveConfig`

All Google Drive / Sheets operations accept an optional [`GDriveConfig`](api/config.md) object. When `None` is passed, a default instance is created.

```python
from gdrive_utils import GDriveConfig

config = GDriveConfig()
```

### Attributes

| Attribute | Default | Description |
|---|---|---|
| `credentials_path` | `secrets/gdrive_credentials.json` | Path to the service-account JSON file. Can be overridden via the `GDRIVE_CREDENTIALS_PATH` environment variable. |
| `spreadsheet_name` | `"DB_calificar_ot"` | Name of the Google Sheet to open. |
| `worksheet_name` | `"Iniciales"` | Name of the worksheet tab inside the sheet. |
| `scope` | `["spreadsheets", "drive"]` | OAuth scopes requested. |

### Environment variable override

```bash
export GDRIVE_CREDENTIALS_PATH=/path/to/credentials.json
```

```python
from gdrive_utils import GDriveConfig

config = GDriveConfig()
assert config.credentials_path == "/path/to/credentials.json"
```

You can still pass an explicit path if needed:

```python
config = GDriveConfig(credentials_path="other.json")
```

## Credentials file

Download a service-account key from [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts) and place it at the path specified by `credentials_path`.

Remember to **share the target Google Sheet** with the service-account email address (visible in the JSON file under `client_email`).
