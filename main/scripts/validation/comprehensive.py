"""Explicit re-export for comprehensive image check."""

from .comprehensive_impl import main as run_check  # noqa: F401

__all__ = ["run_check"]
