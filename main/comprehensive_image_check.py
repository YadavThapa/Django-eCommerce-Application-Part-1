#!/usr/bin/env python
"""Compatibility shim: explicit re-export for comprehensive image check."""

from .scripts.validation.comprehensive import run_check  # noqa: F401

__all__ = ["run_check"]
