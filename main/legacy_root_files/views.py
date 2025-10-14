# -*- coding: utf-8 -*-
"""Legacy shim re-exports for shop views.

This module exists to provide a backward-compatible import
location for older code that expects views to live at
``legacy_root_files.views``. It re-exports selected symbols
from ``shop.views``.
"""

# This file is a tiny, backwards-compatibility shim that only re-exports
# symbols from ``shop.views``. Static checkers (pylint/astroid) can
# sometimes crash or report import errors because this module is a
# runtime-level shim. This file is intentionally a runtime shim; skip
# full static analysis for it to avoid fatal astroid crashes in editors.
# pylint: skip-file

# archived backup - views.py
# moved on 2025-10-07
from main.shop.views import (
    add_to_cart,
    cart,
    cart_detail,
    checkout,
    customer_dashboard,
    home,
    product_detail,
    product_list,
    profile,
    register,
    store_detail,
    store_list,
    vendor_dashboard,
)

__all__ = [
    "home",
    "register",
    "customer_dashboard",
    "profile",
    "product_list",
    "product_detail",
    "add_to_cart",
    "cart",
    "cart_detail",
    "checkout",
    "vendor_dashboard",
    "store_list",
    "store_detail",
]
