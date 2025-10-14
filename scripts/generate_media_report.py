"""Wrapper that forwards to db_tools/generate_media_report.py"""

import os
import sys


def _forward(script_rel: str) -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.join(repo_root, "db_tools", script_rel)
    os.execv(sys.executable, [sys.executable, target] + sys.argv[1:])


if __name__ == "__main__":
    _forward("generate_media_report.py")
