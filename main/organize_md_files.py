#!/usr/bin/env python
"""Tiny safe organizer for Markdown files into docs/."""

from pathlib import Path
import argparse
import os
import shutil


BASE_DIR = Path(r"C:\Users\hemja\OneDrive\Desktop\Django E-commerce")


def organize_md_files(dry_run: bool = False):
    """Move markdown files under BASE_DIR into a central docs/ directory.

    Dry-run mode prints actions without modifying the filesystem.
    """
    docs = BASE_DIR / "docs"
    if not dry_run:
        docs.mkdir(exist_ok=True)

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs if d not in {".venv", "__pycache__", "node_modules", ".git"}
        ]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = Path(root) / f
            rel = str(p.relative_to(BASE_DIR))
            if "docs" in rel.split(os.sep):
                continue
            dest = docs / f
            try:
                if dest.exists() and dest.read_text(
                    encoding="utf-8", errors="ignore"
                ) == p.read_text(encoding="utf-8", errors="ignore"):
                    continue
                if not dry_run:
                    shutil.move(str(p), str(dest))
            except (OSError, PermissionError):
                # Skip files we cannot access or move
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize markdown files into docs/")
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Preview changes only"
    )
    args = parser.parse_args()
    organize_md_files(dry_run=args.dry_run)
