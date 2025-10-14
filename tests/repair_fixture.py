"""Wrapper that forwards to db_tools/repair_fixture.py.

Keeping a thin wrapper at the repository root preserves existing
invocation paths while the canonical implementation lives under
`db_tools/`.
"""

import os
import sys


def _forward(script_name: str) -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    # If invoked from scripts/, repo_root should be the repo root
    if os.path.basename(repo_root) == "scripts":
        repo_root = os.path.dirname(repo_root)
    target = os.path.join(repo_root, "db_tools", script_name)
    os.execv(sys.executable, [sys.executable, target] + sys.argv[1:])


if __name__ == "__main__":
    _forward("repair_fixture.py")
