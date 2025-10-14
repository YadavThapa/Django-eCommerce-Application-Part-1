#!/usr/bin/env python3
"""Safe project organization helpers moved to scripts package."""

# Re-export the implementation from the top-level module to preserve
# backwards compatibility for any code that imported the original path.
from ..safe_organize_project import safe_organize_remaining_files  # noqa: F401


__all__: list[str] = ["safe_organize_remaining_files"]
