"""WSGI config for ecommerce_project project (top-level copy).

This module is a normal WSGI entry point adjusted for the project
living at the repository root under ``ecommerce_project/``. It ensures
the repository root and the ``main/`` package are on sys.path so app
packages like ``shop`` remain importable.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application  # type: ignore

# Add repository root and main/ to sys.path so packages like ``shop``
# are importable.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))

# Use the `main` package settings by default so deployments and WSGI
# hosts use the Postgres-aware configuration (matches manage.py).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

application = get_wsgi_application()
