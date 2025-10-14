"""Shim template tag library to expose 'product_images' under top-level shop.

This module attempts to import the canonical implementation at
`main.shop.templatetags.product_images` and re-exports its public
members. If the canonical implementation isn't importable for some
reason, we provide a tiny fallback implementation that registers a
no-op `product_image` tag so templates depending on it do not fail.

The shim keeps behavior minimal and reversible.
"""

from __future__ import annotations

import importlib
from django import template

register = template.Library()


def _install_fallback():
    """Register a minimal 'product_image' simple_tag fallback.

    The real implementation returns a URL or HTML for a product image.
    Our fallback returns an empty string so pages render without images.
    """

    @register.simple_tag
    def product_image(product):
        # Keep return type predictable for templates.
        return ""


try:
    _real = importlib.import_module("main.shop.templatetags.product_images")
except (ImportError, ModuleNotFoundError):
    # Canonical implementation not available; install fallback.
    _install_fallback()
else:
    # Re-export register and convenience functions from the real module.
    try:
        register = getattr(_real, "register", register)
        product_image = getattr(_real, "product_image")
        # Ensure the function is registered with our local registry if
        # the real module registered it on its own register instance.
        try:
            # If real module used a different Library instance, re-register
            # the callable on our local register to guarantee discovery.
            register.simple_tag(product_image)
        except Exception:
            # If re-registration fails for any reason, ignore and rely on
            # Django's normal tag discovery (the imported module should
            # already have registered the tag under its own module).
            pass
    except Exception:
        # If anything odd happens while re-exporting, fall back to the
        # minimal implementation to avoid breaking templates.
        _install_fallback()
