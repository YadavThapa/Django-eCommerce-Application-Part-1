"""
Compatibility shim: top-level `context_processors.py` proxies to
`shop.context_processors` so templates and legacy imports work.
"""

from shop.context_processors import (
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
]
