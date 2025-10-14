# db_tools — Database utilities

This folder centralizes developer utilities that inspect, migrate, or modify
local databases for the project. The goal is to keep DB-related tooling
in one place while preserving original script invocation paths via
lightweight wrappers in the root `scripts/` and project root.

How to run

  python inspect_postgres.py
  python run_inspect.py
  powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\start_dev_with_postgres.ps1"

Run the canonical files in `db_tools/` directly (recommended):

  python db_tools/print_db_config.py
  python db_tools/inspect_postgres.py
  python db_tools/run_inspect.py
  python db_tools/generate_media_report.py
  python db_tools/sequence_reset_and_verify.py
  python db_tools/backup_and_remove_sqlite.py
  python db_tools/repair_fixture.py

Note: older top-level wrapper scripts have been removed in favor of
calling the canonical files under `db_tools/` to avoid duplication.

Notes
-----
- The scripts expect the Django project to be importable (repo root and
  `main/` are added by many of the scripts) and will set
  `DJANGO_SETTINGS_MODULE` to `main.ecommerce_project.settings` when
  appropriate.

- For running with Postgres, the following environment variables are used
  (the PowerShell helpers under `scripts/` set them for you):

  USE_POSTGRES, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
  POSTGRES_HOST, POSTGRES_PORT

- These utilities are intended for local developer use only and may assume
  development credentials (e.g., `postgres/postgres`). Do not run them
  against production systems without reviewing the code and environment.
