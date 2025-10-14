""" "main" package marker for the project.

Creating this file makes `main` a proper package so package-relative
imports (for example ``from .scripts import ...``) work from modules in
this directory. It's intentionally minimal.
"""

__all__: list[str] = []
