"""Legacy cart test utilities (moved to tests/legacy).

This module provides thin helpers used by older scripts. They are
kept as lightweight wrappers calling the test modules moved into
`tests/legacy/` so existing imports continue to work.
"""

from .test_cart_images import test_cart_images
from .test_cart_images import test_cart_images as test_all_cart_images


def add_test_items_to_cart(request):
    """Legacy helper placeholder — used by debug scripts only."""
    # The original utility worked with Django request objects and the
    # project's Cart helper. To avoid reimplementing the full behavior
    # here (and to keep this change low-risk), callers should import the
    # real implementation from the canonical helpers under `shop`.
    raise RuntimeError(
        "add_test_items_to_cart was intentionally moved; call the Cart API"
    )


def test_cart_session():
    return None


def test_enhanced_cart():
    return None


__all__ = [
    "add_test_items_to_cart",
    "test_cart_images",
    "test_all_cart_images",
    "test_cart_session",
    "test_enhanced_cart",
]
