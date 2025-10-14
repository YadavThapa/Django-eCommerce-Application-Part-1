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

# Ensure command-line runs map the top-level `shop` package to `main.shop`
# early to avoid duplicate Django model registration when code imports both
# module identities. This is a low-risk runtime shim for manage.py only.
try:
    import importlib

    # Make the top-level `shop` package canonical. Import `shop` from the
    # repository root and alias `main.shop` to it so code that still does
    # `from main.shop import ...` resolves to the same module objects.
    try:
        _top_shop = importlib.import_module("shop")
    except Exception:
        _top_shop = None

    import sys as _sys

    if _top_shop is not None:
        _sys.modules.setdefault("shop", _top_shop)
        # If the models submodule exists, map both names to the same module
        try:
            _top_shop_models = importlib.import_module("shop.models")
        except Exception:
            _top_shop_models = None
        _sys.modules.setdefault("main.shop", _top_shop)
        if _top_shop_models is not None:
            _sys.modules.setdefault("shop.models", _top_shop_models)
            _sys.modules.setdefault("main.shop.models", _top_shop_models)
except Exception:
    # If import fails (analysis envs or missing deps), continue normally.
    pass

if __name__ == "__main__":
    # Run administrative tasks.
    # Default to the Postgres-aware settings module in `main/` so local
    # development uses Postgres by default. To fall back to SQLite set
    # DB_ENGINE=sqlite in your environment.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
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
