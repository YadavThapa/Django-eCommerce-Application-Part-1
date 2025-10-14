"""Wrapper forwarding to db_tools/sequence_reset_and_verify.py"""

import os
import sys


def _forward(script_name: str) -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(repo_root) == "scripts":
        repo_root = os.path.dirname(repo_root)
    target = os.path.join(repo_root, "db_tools", script_name)
    os.execv(sys.executable, [sys.executable, target] + sys.argv[1:])


if __name__ == "__main__":
    _forward("sequence_reset_and_verify.py")
