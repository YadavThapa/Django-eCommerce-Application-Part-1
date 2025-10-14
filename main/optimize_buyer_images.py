#!/usr/bin/env python
"""Shim that exposes an explicit function for optimizing buyer images.

The implementation lives in
`main.scripts.utilities.optimize_buyer_images`. This shim exposes
`update_optimal_images` as a clear API for tooling.
"""

from .scripts.validation.optimize_images import (
    update_optimal_images,  # noqa: F401
)

__all__ = ["update_optimal_images"]
