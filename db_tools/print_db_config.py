"""Print environment variables and Django DATABASES for this project.

Copied into db_tools/ so DB-related scripts are centralized. See repo root
README-dev.txt for invocation notes.
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# ensure the repository root and the `main/` package are on sys.path so
# imports like `import shop` succeed the same way they do when running
# through `manage.py` (which inserts these paths).
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
MAIN_PKG = os.path.join(ROOT, "main")
if MAIN_PKG not in sys.path:
    sys.path.insert(0, MAIN_PKG)

env_vars = [
    "USE_POSTGRES",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
]

print("Environment variables:")
for v in env_vars:
    val = os.environ.get(v)
    print(f"{v}={val!r}")

# Ensure Django settings module
# Default to the settings module under `main/` which the project uses
# when started via `manage.py`.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

try:
    import django
    from django.conf import settings
except ImportError as e:
    # ImportError covers ModuleNotFoundError as well; fail-fast if Django
    # isn't available in the environment.
    print("\nDjango import/setup failed:", e)
    print("(Is Django installed in the current Python environment?)")
    sys.exit(2)

try:
    django.setup()
except (
    django.core.exceptions.ImproperlyConfigured,
    django.core.exceptions.AppRegistryNotReady,
) as e:
    # Common failures during setup (misconfiguration or app registry issues).
    # Allow the script to continue so we can still inspect raw settings if possible.
    print("\ndjango.setup() raised:", e)

print("\nDjango DATABASES:")
try:
    print(settings.DATABASES)
except (AttributeError, django.core.exceptions.ImproperlyConfigured) as e:
    print("Failed to read settings.DATABASES:", e)

# Also print which DB engine is selected for convenience
try:
    default = settings.DATABASES.get("default", {})
    engine = default.get("ENGINE")
    name = default.get("NAME")
    print("\nSelected engine:", engine)
    print("Selected NAME:", name)
except (AttributeError, TypeError, KeyError):
    # If settings.DATABASES isn't present or has an unexpected type/shape,
    # just skip the convenience printouts.
    pass
