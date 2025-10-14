"""Copy JSON fixtures from the repository root into db_tools/.

This script is safe to run multiple times. It will not overwrite existing
files unless --overwrite is passed.
"""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_TOOLS = Path(__file__).resolve().parent
DEFAULT_FILES = ["sqlite_data.json", "sqlite_data_clean.json"]


def main(overwrite: bool):
    copied = []
    for fname in DEFAULT_FILES:
        src = ROOT / fname
        dst = DB_TOOLS / fname
        if not src.exists():
            print(f"Skipping {fname}: source not found at {src}")
            continue
        if dst.exists() and not overwrite:
            print(f"Skipping {fname}: destination already exists at {dst}")
            continue
        shutil.copy2(src, dst)
        copied.append((src, dst))
        print(f"Copied {src} -> {dst}")

    if not copied:
        print("No files copied.")
    else:
        print(f"Successfully copied {len(copied)} file(s).")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing files in db_tools/"
    )
    args = p.parse_args()
    main(args.overwrite)
