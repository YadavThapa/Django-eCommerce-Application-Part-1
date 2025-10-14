#!/usr/bin/env python3
"""Top-level shim: expose check_final_assignments.main explicitly."""

from .scripts.validation.check_assignments import (  # noqa: F401
    check_assignments,
)

__all__ = ["check_assignments"]
