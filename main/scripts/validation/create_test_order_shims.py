"""Shims that re-export create_test_order variants explicitly.

This module exposes two named factories used by tests and dev tooling.
"""

from ..tmp_create_test_order import (
    create_test_order as create_test_order_stub,
)  # noqa: F401

from ..tmp_create_test_order2 import (
    create_test_order as create_test_order_runtime,
)  # noqa: F401

__all__ = [
    "create_test_order_stub",
    "create_test_order_runtime",
]
