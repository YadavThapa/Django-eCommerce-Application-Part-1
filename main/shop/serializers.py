"""Shim to the canonical PickleSerializer implementation.

This module is a tiny compatibility shim that re-exports the
PickleSerializer implementation from `shop.utils.serializers` so
existing imports continue to work.

NOTE: Using pickle for session data is insecure for untrusted input. Limit
its use to development/local environments or migrate to JSON for production.
"""

from .utils.serializers import PickleSerializer  # noqa: F401

__all__ = ["PickleSerializer"]
