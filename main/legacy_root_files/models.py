"""Legacy shim re-exports for shop models.

This module provides backward-compatible import paths for older code that
expects models under ``legacy_root_files.models``. It only re-exports
symbols from ``shop.models`` and does not define new runtime behavior.
"""

from shop.models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    PasswordResetToken,
    Product,
    Profile,
    Review,
    Store,
)

__all__ = [
    "Profile",
    "Category",
    "Store",
    "Product",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "Review",
    "PasswordResetToken",
]
