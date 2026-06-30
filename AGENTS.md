# AGENTS.md — Coding conventions for gdrive-utils

> This file contains build steps, testing procedures, and conventions that
> human contributors might not need, but coding agents absolutely do.

---

## Project overview

`gdrive-utils` is a small reusable Python library extracted from the original
`organizar.py` script. It wraps Google Sheets authentication, data retrieval,
and file-renaming operations used in OT (work-order) processing.

The library exposes **two APIs**:

1. **Modern API** — typed functions that accept a `GDriveConfig` and raise
   custom exceptions.
2. **Compatible API** — functions in `compat.py` that preserve the original
   `organizar.py` names and string-based error returns.

---

## Environment

- **Python**: 3.10+ (declared in `.python-version` and `pyproject.toml`)
- **Package manager**: `uv` (Astral). Do **not** use `pip` directly.
- **Working directory**: `/home/vlad/GIT/gdrive_utils` (repo root)

---

## Daily workflow

### Install dependencies

```bash
uv sync --group dev
```

### Run tests

```bash
uv run pytest -v
```

### Lint

```bash
uv run ruff check src tests
```

### Type check

```bash
uv run mypy src
```

### Integration test (manual, requires real Google credentials)

```bash
export GDRIVE_CREDENTIALS_PATH=secrets/gdrive_credentials.json
uv run python scripts/test_integration.py
```

### Build docs locally

```bash
uv run mkdocs serve
```

### Deploy docs to GitHub Pages

```bash
uv run mkdocs gh-deploy --force
```

---

## Architecture

```
src/gdrive_utils/
├── __init__.py       # Public exports (both APIs + exceptions + config)
├── exceptions.py     # Exception hierarchy (GDriveUtilsError base)
├── config.py         # GDriveConfig dataclass
├── auth.py           # google-auth -> gspread client
├── sheets.py         # Google Sheet reading (read_worksheet)
├── core.py           # Pure data processing (modern API)
├── files.py          # File operations (move_file)
├── compat.py         # Backward-compatible wrappers (old API)
└── reader.py         # Placeholder for future Drive reader utilities
```

### Modern API functions (raise exceptions)

| Function | Module | Purpose |
|---|---|---|
| `read_worksheet(config)` | `sheets` | Open configured sheet, return `pd.DataFrame` |
| `get_responsable_order(name, df)` | `core` | Look up `ORDEN_RESPONSABLE` by `NOMBRE` |
| `get_cuadrilla_order(cuad, df)` | `core` | Look up `ORDEN_CUADRILLA` by `CUADRILLA_OT` |
| `get_initials(name, df)` | `core` | Return stored or calculated initials |
| `get_cuadrilla_by_name(name, df)` | `core` | Return `CUADRILLA_OT` by `NOMBRE` |
| `get_short_cuadrilla_name(cuad, df)` | `core` | Return `CUADRILLA_CORTO` or calculated short name |
| `get_all_data(value, column, df)` | `core` | Return full row as dict; `USER_ID` → `int` |
| `build_filename(data, df)` | `core` | Assemble standard OT filename |
| `move_file(src, dst, …)` | `files` | Move file into `ot_procesados/` subdir |

### Compatible API functions (return string error codes)

| Function | Maps to modern | Error returns |
|---|---|---|
| `get_gsheet_df()` | `read_worksheet` | `"Fail"` |
| `get_num_responsable(n, df)` | `get_responsable_order` | `"x"`, `"0"` |
| `get_num_cuadrilla(c, df)` | `get_cuadrilla_order` | `"XX"`, `"no"` |
| `get_iniciales(n, df)` | `get_initials` | `"revisar_nombre"` |
| `from_name_get_cuadrilla(n, df)` | `get_cuadrilla_by_name` | `"no"` |
| `get_nombre_corto_cuadrilla(c, df)` | `get_short_cuadrilla_name` | original string |
| `get_nombre_archivo(obj, df)` | `build_filename` | `os.path.basename(obj.link)` |
| `renombrar_ot(src, dst)` | `move_file` | `"Failed"` |

### Exception hierarchy

```
GDriveUtilsError
├── AuthenticationError
├── SpreadsheetNotFoundError
├── WorksheetNotFoundError
├── DataFrameError
└── FileOperationError
```

---

## Coding conventions

### Docstrings

- **Google style** (Args, Returns, Raises)
- Imperative mood for the summary line
- Leave a blank line after the last section before `"""`

### Type annotations

- Every public function must have typed signatures
- Use `|` union syntax (`str | int`) — Python 3.10+
- Run `mypy src` before committing

### Imports

- Group: stdlib → third-party → local
- Sorted within each group

### Line length

- 100 characters (ruff default in `pyproject.toml`)

### Tests

- Located in `tests/`
- Named `test_<module>.py`
- Use `pytest` fixtures in `conftest.py`
- No docstrings required for test classes/methods (ignored by ruff config)
- Do **not** add integration tests to the pytest discovery path — keep them in
  `scripts/`

---

## DataFrame / sheet schema

The real sheet contains these columns (all strings from gspread, except
`USER_ID` which is an integer):

| Column | Description |
|---|---|
| `ORDEN_RESPONSABLE` | 3-digit hierarchy number (string) |
| `NOMBRE` | Full name, 3–4 words, ALL CAPS (string) |
| `INICIALES` | 2–3 chars, stored or calculated (string) |
| `CUADRILLA_OT` | Official long work-group name (string) |
| `CUADRILLA_CORTO` | Short display name (string) |
| `ORDEN_CUADRILLA` | 2-digit group hierarchy (string) |
| `USER_ID` | Internal organisation number (int32) |
| `CORREO` | E-mail prefix (local-part only), short identifier (string) |

When reading with `read_worksheet()`, all values arrive as strings from
gspread. The `get_all_data()` function converts `USER_ID` to `int`; every
other column (including `CORREO`) is returned as a string.

---

## Configuration

`GDriveConfig` reads the environment variable `GDRIVE_CREDENTIALS_PATH` as a
fallback. The default path is `secrets/gdrive_credentials.json`.

Example:

```python
from gdrive_utils import GDriveConfig

config = GDriveConfig(
    credentials_path="secrets/gdrive_credentials.json",
    spreadsheet_name="DB_calificar_ot",
    worksheet_name="Iniciales",
)
```

---

## Adding a new function

1. Implement in the appropriate `src/gdrive_utils/<module>.py`.
2. Add to `src/gdrive_utils/__init__.py` imports and `__all__`.
3. Add tests in `tests/test_<module>.py`.
4. If the function should also be exposed in the compatible API, add a thin
   wrapper in `compat.py` that catches exceptions and returns string codes.
5. Run `uv run pytest -v`, `uv run ruff check src tests`, `uv run mypy src`.
6. Update `docs/changelog.md`.
7. Commit, push, and redeploy docs if desired.

---

## Release checklist

1. Update version in `pyproject.toml` (if bumping).
2. Update `docs/changelog.md`.
3. Commit and push to `master`.
4. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z`
5. Deploy docs: `uv run mkdocs gh-deploy --force`

---

## Git workflow

- Branch: `master` (default)
- Do **not** use `git commit --amend` or force-push unless explicitly asked.
- Ask before creating pull requests (this is a personal repo).

---

## CI

GitHub Actions workflow at `.github/workflows/ci.yml` runs on push/PR:
- `ruff check`
- `mypy src`
- `pytest -v`

It does **not** run integration tests (no credentials in CI).

---

## Common pitfalls

- `oauth2client` is **deprecated** — the library uses `google-auth`.
- The `compat.py` wrappers must **never** change return types (strings only).
- `site/` and `.coverage` are in `.gitignore` — do not commit build artifacts.
- `organizar.py` is kept in the repo for reference but is **not** the source of
  truth anymore.
