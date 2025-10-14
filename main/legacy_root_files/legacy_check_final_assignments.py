"""Archived: lightweight shim for the legacy check_final_assignments script.

This file intentionally raises if executed; it serves as a lightweight
placeholder that points maintainers to the full script in the
`legacy_root_files/` directory to avoid accidental execution of
outdated scripts.
"""


def main(*a, **k):
    """Placeholder entrypoint that directs users to the archived script.

    The function raises deliberately so that automated tooling doesn't
    accidentally run the legacy implementation.
    """
    raise RuntimeError(
        "See legacy_root_files/check_final_assignments.py for the full script"
    )


__all__ = ["main"]
