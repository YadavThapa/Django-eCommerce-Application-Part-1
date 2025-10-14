"""
Compatibility shim for `shop.utils` package. Re-exports public symbols from
`main.utils` to support legacy imports while the canonical code lives under `main`.
"""
try:
    # Re-export everything from main.utils if available
    from main.utils import *  # noqa: F401,F403
    try:
        from main.utils import __all__ as __all__  # type: ignore
    except Exception:
        pass
except Exception:
    # Minimal fallbacks to avoid import-time crashes in environments where
    # the main package isn't present (editor analysis, etc.).
    __all__ = []
