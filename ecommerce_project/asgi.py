"""ASGI config for ecommerce_project project (top-level copy)."""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application  # type: ignore

# Add repo root and main/ to sys.path so app imports work.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")

application = get_asgi_application()
