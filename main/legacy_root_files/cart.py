"""Archived shim: re-export of the legacy top-level `cart.Cart`.

This file is kept for historical/reference reasons. It re-exports the
`Cart` class from `shop.cart` so code that imported the legacy path
continues to work during transition.
"""

from main.shop.cart import Cart  # noqa: F401

__all__ = ["Cart"]
