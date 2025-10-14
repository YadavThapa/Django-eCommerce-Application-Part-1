#!/usr/bin/env python3
"""Compatibility shim for check_final_assignments moved to scripts.

This module re-exports the current implementation. Historically callers
imported `main` from this path; provide a `main` alias for backward
compatibility while importing the canonical name from the top-level
module.
"""

from ..check_final_assignments import check_assignments  # noqa: F401

# Backwards-compatible alias used by older callers/tests.
main = check_assignments


__all__: list[str] = ["check_assignments", "main"]
