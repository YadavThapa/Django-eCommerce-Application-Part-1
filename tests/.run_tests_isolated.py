"""Run Django tests with an isolated sys.path that contains only the `main/` package.

This avoids importing the top-level `shop` package directory and ensures
`import shop` resolves to `main.shop` when run as a package.
"""

import os
import sys
import importlib
from types import ModuleType

ROOT = os.path.dirname(os.path.abspath(__file__))
MAIN_PATH = os.path.join(ROOT, "main")

# Ensure the repo root is NOT on sys.path so the top-level `shop` package
# directory at the repository root isn't importable. Then insert the
# `main/` package directory at the front so imports resolve to `main.*`.
root_abs = os.path.abspath(ROOT)
main_abs = os.path.abspath(MAIN_PATH)
# Remove any existing occurrences of these paths to control ordering
sys.path[:] = [p for p in sys.path if os.path.abspath(p) not in (root_abs, main_abs)]
# Insert MAIN_PATH first so `import main.*` resolves correctly
sys.path.insert(0, main_abs)
# Then insert the repo root so package names like `main` still resolve and
# other top-level tools that rely on the repo root can import.
if root_abs != main_abs:
    sys.path.insert(1, root_abs)

# Import `main.shop` early and alias it to the top-level `shop` module name so
# when Django imports INSTALLED_APPS entries like 'shop' it will use the
# already-loaded `main.shop` module instead of loading the repo-root `shop`.
# Keep exceptions narrow so linters don't complain about broad catches.
main_shop: ModuleType | None = None
try:
    main_shop = importlib.import_module("main.shop")
    sys.modules.setdefault("shop", main_shop)
    # Do NOT import `main.shop.models` here: importing models may access
    # Django settings and cause ImproperlyConfigured before we call
    # django.setup(). We only alias the package module itself.
except ImportError:
    # If importing main.shop fails, continue and let Django's normal import
    # flow raise the appropriate error during test execution.
    main_shop = None

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

# Alias module names again after setting DJANGO_SETTINGS_MODULE. Use narrow
# exceptions so tooling flags are reduced.
try:
    if main_shop is None:
        main_shop = importlib.import_module("main.shop")
        # Ensure the top-level name 'shop' maps to the same module object
        sys.modules["shop"] = main_shop
    # Avoid importing `main.shop.models` before django.setup() for the same
    # reason as above. The app registry will import models at the correct
    # time when Django initializes.
except ImportError:
    # Let Django handle import errors at runtime
    pass

import django  # type: ignore  # noqa: E402
from django.core.management import call_command  # type: ignore  # noqa: E402

# Setup Django and run the requested tests. Errors should propagate to the
# caller so CI / the developer sees them.
django.setup()
# After Django is configured, import the package using the top-level name
# ("shop") so Python creates a single set of module objects rooted at
# 'shop'. Then map the legacy package names (like 'main.shop' and
# 'main.shop.models') to the same module objects. Importing via the
# top-level name first avoids creating separate objects for the same
# file under different module names which leads to duplicate model
# registration in Django.
try:
    # Import the package as the top-level name so the module objects are
    # created under 'shop' and its submodules.
    shop_pkg = importlib.import_module("shop")
    shop_models = importlib.import_module("shop.models")

    # Make sure both naming paths point to the exact same module objects.
    sys.modules["shop"] = shop_pkg
    sys.modules["shop.models"] = shop_models

    # Also map the 'main.*' names to the same objects so code importing
    # either name gets identical modules.
    sys.modules["main.shop"] = shop_pkg
    sys.modules["main.shop.models"] = shop_models
except (ImportError, RuntimeError):
    # If preload fails, let the test run trigger import or registry errors
    # so the developer sees them. We only catch import/runtime issues here.
    pass
call_command("test", "main.tests.test_smoke", verbosity=2)
