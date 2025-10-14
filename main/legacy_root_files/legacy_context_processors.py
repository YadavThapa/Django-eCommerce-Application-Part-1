"""Archived context_processors shim (legacy copy)."""

# Legacy shim - silence linters for wildcard re-export
# pylint: skip-file
# flake8: noqa
# type: ignore

from main.shop.context_processors import (
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
