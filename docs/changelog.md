# Changelog

## 0.2.0 (2026-06-28)

### Added

- `get_all_data(value, column, df)` — look up a full row by any column and
  receive every field as a dictionary. `USER_ID` is returned as `int`; all
  other fields are strings. Raises `DataFrameError` if the column is missing
  or no match is found.

## 0.1.0 (2026-06-28)

### Added

- Initial release extracted from `organizar.py`.
- Modern API with typed exceptions and `GDriveConfig`.
- Compatible API preserving original function names and string error returns.
- Google-auth authentication (replaced deprecated `oauth2client`).
- Test suite with `pytest` and coverage reporting.
- CI pipeline via GitHub Actions.
- Documentation site powered by MkDocs + Material + mkdocstrings.
