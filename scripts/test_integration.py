#!/usr/bin/env python3
"""Manual integration test for gdrive-utils against a real Google Sheet.

This script is **not** run by pytest or CI.  Execute it locally after
exporting your credentials path:

    export GDRIVE_CREDENTIALS_PATH=secrets/gdrive_credentials.json
    uv run python scripts/test_integration.py

Exit codes
----------
* 0 — all checks passed
* 1 — a check failed (see printed output)
* 2 — credentials file not found or authentication failed

"""

import os
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def _section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    _section("gdrive-utils Integration Test")

    # 1. Credentials
    creds_path = os.getenv("GDRIVE_CREDENTIALS_PATH", "secrets/gdrive_credentials.json")
    print(f"\n1. Credentials file")
    print(f"   Expected: {creds_path}")
    if not os.path.exists(creds_path):
        _fail(f"File not found: {creds_path}")
        print("\n   Tip: export GDRIVE_CREDENTIALS_PATH=/path/to/credentials.json")
        return 2
    _ok("Credentials file exists")

    # 2. Authentication
    print("\n2. Authentication")
    try:
        from gdrive_utils import GDriveConfig, read_worksheet
        from gdrive_utils.core import (
            get_all_data,
            get_cuadrilla_order,
            get_initials,
            get_responsable_order,
            get_short_cuadrilla_name,
        )
        from gdrive_utils.exceptions import GDriveUtilsError
    except ImportError as exc:
        _fail(f"Cannot import gdrive_utils: {exc}")
        return 1

    config = GDriveConfig()
    try:
        df = read_worksheet(config)
    except GDriveUtilsError as exc:
        _fail(f"Authentication or sheet access failed: {exc}")
        return 2
    _ok(f"Authenticated and read worksheet: {len(df)} rows")

    # 3. Column validation
    print("\n3. Expected columns")
    expected_cols = [
        "NOMBRE",
        "INICIALES",
        "ORDEN_RESPONSABLE",
        "CUADRILLA_OT",
        "CUADRILLA_CORTO",
        "ORDEN_CUADRILLA",
        "USER_ID",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        _fail(f"Missing columns: {missing}")
    else:
        _ok(f"All {len(expected_cols)} expected columns present")

    # 4. Functional checks
    print("\n4. Functional checks")
    errors = 0

    # 4a. get_all_data by NOMBRE
    try:
        first_name = df.iloc[0]["NOMBRE"]
        row_data = get_all_data(first_name, "NOMBRE", df)
        assert isinstance(row_data, dict)
        assert "USER_ID" in row_data
        assert isinstance(row_data["USER_ID"], int)
        assert all(isinstance(v, str) for k, v in row_data.items() if k != "USER_ID")
        _ok(f"get_all_data('{first_name}', 'NOMBRE') -> USER_ID={row_data['USER_ID']}")
    except Exception as exc:
        _fail(f"get_all_data by NOMBRE: {exc}")
        errors += 1

    # 4b. get_all_data by INICIALES
    try:
        first_initials = df.iloc[0]["INICIALES"]
        row_data = get_all_data(first_initials, "INICIALES", df)
        assert row_data["INICIALES"] == first_initials
        _ok(f"get_all_data('{first_initials}', 'INICIALES') -> NOMBRE={row_data['NOMBRE']}")
    except Exception as exc:
        _fail(f"get_all_data by INICIALES: {exc}")
        errors += 1

    # 4c. get_responsable_order
    try:
        first_name = df.iloc[0]["NOMBRE"]
        order = get_responsable_order(first_name, df)
        assert isinstance(order, str)
        _ok(f"get_responsable_order('{first_name}') -> {order}")
    except Exception as exc:
        _fail(f"get_responsable_order: {exc}")
        errors += 1

    # 4d. get_initials
    try:
        first_name = df.iloc[0]["NOMBRE"]
        initials = get_initials(first_name, df)
        assert isinstance(initials, str)
        _ok(f"get_initials('{first_name}') -> {initials}")
    except Exception as exc:
        _fail(f"get_initials: {exc}")
        errors += 1

    # 4e. get_short_cuadrilla_name
    try:
        first_cuad = df.iloc[0]["CUADRILLA_OT"]
        short = get_short_cuadrilla_name(first_cuad, df)
        assert isinstance(short, str)
        _ok(f"get_short_cuadrilla_name('{first_cuad}') -> {short}")
    except Exception as exc:
        _fail(f"get_short_cuadrilla_name: {exc}")
        errors += 1

    # 5. Summary
    _section("Summary")
    if errors == 0:
        print("All integration checks passed!")
        return 0
    print(f"{errors} check(s) failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
