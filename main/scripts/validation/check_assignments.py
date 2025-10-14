"""Explicit re-export for checking final assignments."""

from .check_assignments_impl import main as check_assignments  # noqa: F401

__all__ = ["check_assignments"]
