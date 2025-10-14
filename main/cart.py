"""Compatibility shim: re-export Cart from shop.cart

This module is a lightweight shim left at project root so existing imports
like `from cart import Cart` continue to work after repository cleanup.
It intentionally contains no business logic.
"""

from main.shop.cart import Cart  # noqa: F401

__all__ = ["Cart"]
