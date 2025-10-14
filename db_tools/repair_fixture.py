"""Utility to repair encoding of fixtures dumped from sqlite3.

Copied into db_tools/ to centralize fixture and DB-related utilities.
"""

import sys
from pathlib import Path


DEFAULT_IN = "sqlite_data.json"
DEFAULT_OUT = "sqlite_data_clean.json"


def repair_fixture(in_file: str | None = None, out_file: str | None = None) -> int:
    """Repair encoding of a JSON fixture.

    By default operates on the fixture files that live in the same folder as
    this script (the canonical copies under db_tools/). Returns exit code.
    """
    db_tools_dir = Path(__file__).resolve().parent
    in_path = db_tools_dir / (in_file or DEFAULT_IN)
    out_path = db_tools_dir / (out_file or DEFAULT_OUT)

    if not in_path.exists():
        print("Input file not found:", in_path)
        return 2

    raw = in_path.read_bytes()

    encodings = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        "latin-1",
    ]

    text: str | None = None
    for enc in encodings:
        try:
            text = raw.decode(enc)
            print("Decoded using", enc)
            break
        except UnicodeDecodeError:
            text = None
    else:
        print("Failed to decode with common encodings; aborting")
        return 3

    # Normalize newlines and strip BOM if any remained
    if text is not None and text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    out_path.write_text(text or "", encoding="utf-8")
    print("Wrote cleaned fixture to", out_path)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point wrapper: parse optional argv and run repair_fixture.

    Accepts two optional positional arguments: <input-file> <output-file>.
    When omitted the defaults inside `db_tools/` are used.
    Returns an exit code integer suitable for SystemExit.
    """
    argv = argv or sys.argv[1:]
    if len(argv) >= 1:
        in_file = argv[0]
    else:
        in_file = None
    if len(argv) >= 2:
        out_file = argv[1]
    else:
        out_file = None
    return repair_fixture(in_file, out_file)


if __name__ == "__main__":
    raise SystemExit(main())
