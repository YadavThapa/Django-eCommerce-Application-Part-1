"""Load the `main` package explicitly and alias `shop` to `main.shop` before Django loads.

This avoids importing the top-level `shop` package separately and prevents duplicate
Django model registration caused by the same file being loaded under two module
names (e.g., 'shop.models' and 'main.shop.models').
"""

import importlib
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(ROOT, "main")
MAIN_INIT = os.path.join(MAIN_DIR, "__init__.py")

# Load 'main' package explicitly from main/__init__.py
spec = importlib.util.spec_from_file_location("main", MAIN_INIT)
main_mod = importlib.util.module_from_spec(spec)
sys.modules["main"] = main_mod
spec.loader.exec_module(main_mod)

# Ensure subpackage directory is on sys.path for imports of submodules
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

# Import main.shop and alias it as top-level 'shop'
try:
    main_shop = importlib.import_module("main.shop")
    sys.modules.setdefault("shop", main_shop)
    try:
        main_shop_models = importlib.import_module("main.shop.models")
        sys.modules.setdefault("shop.models", main_shop_models)
    except Exception:
        pass
except Exception:
    # If this fails, let Django's import flow produce the error
    pass

# Now run Django test command. The following imports are intentionally
# done after setting DJANGO_SETTINGS_MODULE so Django can be configured
# before import; silence E402 for this deliberate ordering.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
import django  # noqa: E402
from django.core.management import call_command  # noqa: E402

django.setup()
call_command("test", "main.tests.test_smoke", verbosity=2)
