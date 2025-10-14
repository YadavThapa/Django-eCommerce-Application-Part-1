r"""
Runner to execute script-style test files under the top-level `tests/` directory as
standalone programs. Saves per-script stdout/stderr to test_script_outputs/<relpath>.out and
returns non-zero exit code if any script fails.

Usage:
    .venv\Scripts\python.exe scripts/run_test_scripts.py

This intentionally treats each file as an executable verification script (they call
django.setup() inside), avoiding pytest collection import-time DB issues.
"""

import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[0]
REPO_ROOT = ROOT.parent
SCRIPTS_DIR = REPO_ROOT / "tests"
OUT_DIR = REPO_ROOT / "test_script_outputs"

PY = sys.executable


def find_scripts():
    return sorted([p for p in SCRIPTS_DIR.rglob("*.py") if p.is_file()])


def run_script(path: Path) -> int:
    rel = path.relative_to(REPO_ROOT)
    out_path = OUT_DIR / (str(rel).replace("\\", "/") + ".out")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Prepare subprocess environment: ensure DJANGO_SETTINGS_MODULE points
    # to the project's settings package under `main`, and run with
    # unbuffered output so we capture streaming prints.
    env = dict(**os.environ)
    env.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
    env.setdefault("PYTHONUNBUFFERED", "1")
    # Ensure stdout/stderr use UTF-8 encoding so Unicode (e.g. checkmark emojis)
    # printed by scripts don't raise UnicodeEncodeError on Windows consoles.
    env.setdefault("PYTHONIOENCODING", "utf-8")
    # Ensure subprocess can import top-level packages by adding repo root to PYTHONPATH
    env.setdefault("PYTHONPATH", str(REPO_ROOT))

    with out_path.open("wb") as f:
        f.write(f"--- RUN: {rel}\n".encode())
        f.write(b"--- CMD: ")
        f.write((PY + " \"" + str(path) + "\"\n").encode())
        f.write(b"--- OUTPUT ---\n")

        # Run the script with the repository root as the working directory so
        # package imports that expect the repo root on sys.path (e.g. `import main`)
        # resolve correctly when running as a script.
        proc = subprocess.Popen(
            [PY, str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(REPO_ROOT),
            env=env,
        )
        if proc.stdout is not None:
            for chunk in proc.stdout:
                if chunk:
                    f.write(chunk)
        proc.wait()
        f.write(b"\n--- EXIT CODE: ")
        f.write(str(proc.returncode).encode())
        f.write(b"\n")
    return proc.returncode


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    scripts = find_scripts()
    if not scripts:
        print("No scripts found under", SCRIPTS_DIR)
        return 0

    failures = []
    for s in scripts:
        print("Running:", s)
        rc = run_script(s)
        if rc != 0:
            failures.append((s, rc))

    print("\nSummary:")
    print(f"  Total scripts: {len(scripts)}")
    print(f"  Failures: {len(failures)}")
    for s, rc in failures:
        print(f"    - {s} -> exit {rc}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
