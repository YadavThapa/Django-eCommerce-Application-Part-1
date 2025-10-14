"""Launcher stub — delegates to `tests/test_postgres_and_http_mainsettings.py`."""
from importlib import import_module


def main() -> None:
    import_module("tests.test_postgres_and_http_mainsettings")


if __name__ == "__main__":
    main()
