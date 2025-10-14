"""WSGI config for ecommerce_project project.

This module exposes the WSGI callable as a module-level variable named
``application``. The imports are grouped and placed at the top to satisfy
linters while preserving the original runtime behavior.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application  # type: ignore


# Add repository root and `main/` to sys.path so packages are importable.
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "main.ecommerce_project.settings",
)


application = get_wsgi_application()
