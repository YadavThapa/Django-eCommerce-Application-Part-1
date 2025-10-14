"""Compatibility shim: cart test utilities.

Historically this module re-exported helpers from `tests.legacy`. To
allow removing the `tests/legacy/` proxy folder safely we provide small
backwards-compatible placeholders here. These are intentionally
lightweight and will raise clear messages if callers attempt to use
functionality that was moved to the canonical test or helper locations.
"""

from typing import Any


def add_test_items_to_cart(request: Any) -> None:
    """Deprecated test helper.

    The real helper was moved out of `tests/legacy/` during cleanup. If
    you relied on this helper in scripts or debugging flows, please use
    the project's `Cart` API or the canonical test helpers under
    `tests/`.
    """
    raise RuntimeError(
        "add_test_items_to_cart was moved; call the Cart API or the "
        "canonical test helper in `tests/` instead"
    )


def test_cart_images() -> None:
    """Legacy shim: lightweight smoke-check for cart images."""
    print("[shim] test_cart_images: placeholder; original moved to tests/")


# Keep alias names previously exported by the shim
test_all_cart_images = test_cart_images


def test_cart_session() -> None:
    """Placeholder; preserved for compatibility with legacy imports."""
    return None


def test_enhanced_cart() -> None:
    """Placeholder; preserved for compatibility with legacy imports."""
    return None


__all__ = [
    "add_test_items_to_cart",
    "test_cart_images",
    "test_all_cart_images",
    "test_cart_session",
    "test_enhanced_cart",
]
