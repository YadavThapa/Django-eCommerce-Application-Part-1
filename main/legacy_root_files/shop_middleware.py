"""Legacy shim re-exporting middleware from shop.shop_middleware.

Kept for compatibility with older imports; re-exports a small set of
middleware classes used around the project.
"""

from main.shop.shop_middleware import (
    PermissionMiddleware,
    SecurityMiddleware,
    UserActivityMiddleware,
)

__all__ = [
    "PermissionMiddleware",
    "SecurityMiddleware",
    "UserActivityMiddleware",
]
