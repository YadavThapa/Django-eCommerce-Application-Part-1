#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path

# Ensure both the repository root and `main/` are on sys.path so imports
# like `main.ecommerce_project` and top-level app imports (e.g. `shop`)
# remain importable regardless of import style used by scripts.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))

# NOTE: We deliberately avoid importing the `shop` package or its
# submodules at module import time because that can trigger Django model
# imports which require settings to be configured. Alias setup is
# performed later in ``__main__`` once DJANGO_SETTINGS_MODULE is set.

if __name__ == "__main__":
    # Run administrative tasks.
    # Default to the Postgres-aware settings module in `main/` so local
    # development uses Postgres by default. To fall back to SQLite set
    # DB_ENGINE=sqlite in your environment.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
    # Note: we intentionally avoid importing the `shop` package or its
    # submodules from manage.py. Importing those modules can trigger
    # Django model code that requires the app registry to be ready and
    # would raise during startup. The lightweight top-level shim in
    # `shop/__init__.py` provides editor/runtime compatibility without
    # causing early imports; leave aliasing to that mechanism.
    try:
        # Import inside main to avoid editor/runtime ordering issues
        # for this runtime-only import.
        from django.core.management import (
            execute_from_command_line,  # type: ignore[import]
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
