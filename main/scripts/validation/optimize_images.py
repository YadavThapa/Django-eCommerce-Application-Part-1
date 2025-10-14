"""Validation wrapper for optimize_buyer_images.

Expose a named function `update_optimal_images` that tooling can call.
The implementation lives in `main.scripts.utilities.optimize_buyer_images`.
"""


def update_optimal_images() -> None:
    """Import and run the implementation.

    If the implementation module exposes a callable `run` we call it.
    Otherwise importing the module may execute the top-level script
    behaviour (many maintenance scripts do this).
    """
    # Import at runtime to avoid importing Django-dependent modules at
    # import-time. Static checkers will complain about imports inside
    # functions; silence with a local type-ignore when necessary.
    # pylint: disable=import-outside-toplevel
    from ..utilities import optimize_buyer_images as impl  # type: ignore

    if hasattr(impl, "run"):
        impl.run()
    else:
        # Importing the module is sufficient for scripts that execute on
        # import; keep a reference to avoid linter complaints.
        _ = impl


__all__ = ["update_optimal_images"]
