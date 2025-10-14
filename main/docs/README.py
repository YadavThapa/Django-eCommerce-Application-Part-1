"""Local development README (minimal).

Use this module to print a short usage note when executed directly.
It is intentionally minimal and ASCII-only to avoid lint and syntax
issues in automated environments.
"""

# The filename `README.py` intentionally uses upper-case; silence the
# module-name invalid-name warning from pylint for this doc-only module.
# pylint: disable=invalid-name

if __name__ == "__main__":
    import logging

    logging.getLogger(__name__).info(__doc__)
