"""Legacy shim: re-export commonly used context processors.

This file is kept as an archived compatibility shim. It re-exports a small set
of context processor callables used across older templates and code paths.

Converted tabs to spaces and added a module docstring to quiet static-
analysis warnings (W191 / missing-module-docstring).
"""

from shop.context_processors import (
    _get_user_dashboard_url,
    auth_context,
    breadcrumb_context,
    navigation_context,
    permissions_context,
)

__all__ = [
    "auth_context",
    "permissions_context",
    "navigation_context",
    "breadcrumb_context",
    "_get_user_dashboard_url",
]
