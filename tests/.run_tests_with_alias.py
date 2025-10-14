"""Temporary test runner that aliases top-level `shop` to `main.shop` before
imports so the Django app loads under a single module identity.

Usage: python .run_tests_with_alias.py
"""

import os
import sys
import importlib

# Ensure repo root and main are on sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
MAIN_PATH = os.path.join(ROOT, "main")
if MAIN_PATH not in sys.path:
    sys.path.insert(0, MAIN_PATH)

# Point Django settings at the project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

# Try to import main.shop and alias it as shop
try:
    main_shop = importlib.import_module("main.shop")
    sys.modules.setdefault("shop", main_shop)
    # Also map shop.models if available
    try:
        ms = importlib.import_module("main.shop.models")
        sys.modules.setdefault("shop.models", ms)
    except Exception:
        pass
except Exception:
    # If we can't import main.shop yet, continue; the alias may still help
    pass

# Run Django test command. These imports are intentionally deferred until
# after DJANGO_SETTINGS_MODULE is set; silence E402 for the deliberate order.
import django  # noqa: E402
from django.core.management import call_command  # noqa: E402

django.setup()

# Run the targeted smoke test
exit_code = 1
try:
    call_command("test", "main.tests.test_smoke", verbosity=2)
    exit_code = 0
except SystemExit as se:
    # call_command might call sys.exit
    exit_code = int(se.code or 0)
except Exception:
    import traceback

    traceback.print_exc()
    exit_code = 2

sys.exit(exit_code)
