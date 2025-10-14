"""Lightweight placeholder for the legacy comprehensive image check.

This module intentionally acts as a shim that points maintainers at the
full implementation in the repository. It raises if executed to avoid
accidental runs of archived code.
"""


def run(*a, **k):
    """Placeholder entrypoint that documents where the real script lives.

    Raising here prevents outdated legacy code from being executed by
    accident during automated maintenance runs.
    """
    raise RuntimeError(
        "See comprehensive_image_check.py in the legacy folder "
        "for the implementation"
    )


__all__ = ["run"]
