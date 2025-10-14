"""
Compatibility shim: top-level `shop_middleware.py` now proxies to
`shop.shop_middleware` inside the package.
"""

# Shim for compatibility: re-export the package's middleware. Silence
# linters for this small proxy so static analyzers don't raise
# spurious warnings about unused re-exports.
# pylint: skip-file
# flake8: noqa
# type: ignore

from shop.shop_middleware import (
    MiddlewareMixin,
    PermissionMiddleware,
    SecurityMiddleware,
    UserActivityMiddleware,
    messages,
    redirect,
)

__all__ = [
    "MiddlewareMixin",
    "PermissionMiddleware",
    "SecurityMiddleware",
    "UserActivityMiddleware",
    "messages",
    "redirect",
]
