"""Launcher stub — delegates to `tests/test_postgres_and_http.py`.

The real test script lives in `tests/`. Keeping this small wrapper
maintains backward compatibility for any external references.
"""

import os
import sys
from importlib import import_module

# Ensure project root is on path
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

try:
    import django  # type: ignore
    django.setup()
except Exception as e:
    print('Failed to set up Django:', e)
    raise


def main() -> None:
    import_module("tests.test_postgres_and_http")


if __name__ == "__main__":
    main()
