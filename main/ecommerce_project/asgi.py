"""ASGI config for ecommerce_project project.

This module exposes the ASGI callable as a module-level variable named
``application``. Imports are grouped at the top to satisfy linters while
preserving original runtime behavior.
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application  # type: ignore


# Ensure repository root and `main/` are on sys.path so app packages are
# importable under ASGI.
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "main.ecommerce_project.settings",
)


application = get_asgi_application()
