"""Package marker for top-level shop.templatetags shims.

This package exists to allow Django to discover template tag libraries
under the top-level `shop` package while we canonicalize modules under
`main.shop`. It intentionally has no side-effects.
"""

__all__ = []
