"""Forwarding urls module so include('shop.urls') resolves to main.shop.urls.

This module attempts to import the real urlconf from `main.shop.urls` and
re-export its attributes. If that import fails, it defines a tiny fallback
urlpatterns to avoid import errors during early startup.
"""

from __future__ import annotations

import importlib

try:
    _real = importlib.import_module("main.shop.urls")
    # Re-export commonly used names (urlpatterns, handler404/500, etc.)
    urlpatterns = getattr(_real, "urlpatterns", [])
    handler404 = getattr(_real, "handler404", None)
    handler500 = getattr(_real, "handler500", None)
    handler403 = getattr(_real, "handler403", None)
    handler400 = getattr(_real, "handler400", None)
    # Expose app_name so include('shop.urls') registers the namespace
    app_name = getattr(_real, "app_name", "shop")
except (ImportError, ModuleNotFoundError):
    # Minimal safe fallback so Django's include/import machinery doesn't fail
    urlpatterns = []
    handler404 = handler500 = handler403 = handler400 = None
