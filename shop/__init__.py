"""Runtime shim package to make top-level `shop` import identity point to `main.shop`.

This keeps existing imports like `import shop` or `include('shop.urls')`
working while the codebase canonicalizes modules under `main.shop`.

This shim deliberately keeps logic minimal and safe: it attempts to import
`main.shop` and, if successful, installs it in sys.modules under the name
`shop`. If anything goes wrong we fall back to being a normal empty package
so Django's import machinery can still import submodules that exist under
the `shop/` shim directory.
"""

from __future__ import annotations

import importlib
import sys

try:
    _main_shop = importlib.import_module("main.shop")
    # Make the main.shop module available as top-level 'shop'
    sys.modules.setdefault("shop", _main_shop)
except (ImportError, ModuleNotFoundError):
    # If main.shop isn't importable yet, behave like a normal package and
    # allow Python to find other submodules under this directory (e.g. shop.urls).
    # We intentionally do not swallow other exceptions here to avoid masking
    # unexpected runtime errors during startup.
    pass
# Package marker: keep the package importable without side-effects.
__all__: list[str] = []
