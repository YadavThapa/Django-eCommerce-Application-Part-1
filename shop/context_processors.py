"""Shim forwarding to main.shop.context_processors.

This keeps settings like "shop.context_processors.auth_context" working while
the codebase canonicalizes modules under main.shop.
"""

from __future__ import annotations

try:
    from main.shop.context_processors import (
        auth_context,
        permissions_context,
        navigation_context,
        breadcrumb_context,
        _get_user_dashboard_url,
    )

    __all__ = [
        "auth_context",
        "permissions_context",
        "navigation_context",
        "breadcrumb_context",
        "_get_user_dashboard_url",
    ]
except (ImportError, ModuleNotFoundError):
    # Provide safe fallbacks to avoid import errors during early startup.
    def auth_context(request):
        return {}

    def permissions_context(request):
        return {}

    def navigation_context(request):
        return {"nav_items": []}

    def breadcrumb_context(request):
        return {"breadcrumbs": []}

    def _get_user_dashboard_url(user):
        return None

    __all__ = [
        "auth_context",
        "permissions_context",
        "navigation_context",
        "breadcrumb_context",
        "_get_user_dashboard_url",
    ]
