"""Diagnose why `import shop` may fail in this workspace.

Prints sys.path, lists top-level directories in the repo root, and attempts to import `shop`.
"""

import os
import sys
import importlib as _importlib
from importlib import util as importlib_util  # type: ignore


def main() -> None:
    """Run diagnostics which attempt to import the project's `shop` package.

    Prints sys.path, repo entries, attempts to locate and import `shop`, and
    reports candidate filesystem locations. This helps diagnose import errors
    when running helper scripts from the `scripts/` directory.
    """
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("Repo root:", root)
    print("\nFirst entries of sys.path:")
    for p in sys.path[:10]:
        print(" -", p)

    print("\nIs repo root on sys.path?", root in sys.path)

    print("\nTop-level directories/files in repo root:")
    for name in sorted(os.listdir(root)):
        print(" -", name)

    print("\nAttempting import of shop:")
    # Try to locate the module spec using importlib.util when available.
    try:
        shop_spec = importlib_util.find_spec("shop")
    except (ImportError, AttributeError):
        shop_spec = None
    print("find_spec for shop:", shop_spec)

    # Attempt to import the package and report its location.
    try:
        shop = _importlib.import_module("shop")
        print("Imported shop from", getattr(shop, "__file__", repr(shop)))
    except ModuleNotFoundError as e:
        print("Import failed:", type(e).__name__, e)
    except Exception as e:  # pylint: disable=broad-except
        # Catch other import-related errors (e.g. runtime errors during import).
        # We deliberately allow a broad catch here so the diagnostic prints
        # the exception type and message instead of crashing the script.
        print("Import raised during execution:", type(e).__name__, e)

    # Also try to locate shop package in common locations
    candidates = [
        os.path.join(root, "shop"),
        os.path.join(root, "main", "shop"),
    ]
    print("\nCandidate locations:")
    for c in candidates:
        print(" -", c, "exists" if os.path.exists(c) else "missing")


if __name__ == "__main__":
    main()
