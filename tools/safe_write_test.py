"""Launcher stub — uses the copy in `tests/`.

This file was preserved as a small wrapper so external scripts that call
`tools.safe_write_test` keep working. The real test lives at
`tests/safe_write_test.py`.
"""
from importlib import import_module


def main() -> None:
    """Import and (optionally) run the real safe-write test in `tests/`.

    The wrapper preserves backward compatibility for callers that import
    ``tools.safe_write_test``. If the tests module exposes a ``main``
    callable we call it; otherwise we only import the module so any top
    level registration code runs.
    """
    mod = import_module("tests.safe_write_test")
    main_fn = getattr(mod, "main", None)
    if callable(main_fn):
        main_fn()


if __name__ == "__main__":
    main()
