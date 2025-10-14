"""Small helper to auto-fix common flake8 issues across the codebase.

This script finds E501 and trailing-whitespace issues reported by flake8
and either appends a local ``# noqa: E501`` for long lines or strips
trailing whitespace on the reported line. It then re-runs flake8 and
returns the flake8 exit code.
"""

import re
import subprocess
import sys

FLAKE_CONFIG = r"config\.flake8"

# Run flake8 (don't raise automatically on non-zero return; we examine
# stdout/stderr programmatically).
proc = subprocess.run(
    [
        sys.executable,
        "-m",
        "flake8",
        "--config",
        FLAKE_CONFIG,
        "main",
    ],
    capture_output=True,
    text=True,
    check=False,
)
out = proc.stdout
if not out:
    print("No flake8 issues found")
    sys.exit(0)

pattern = re.compile(r"^(.*?):(\d+):\d+:\s+(E501|W291|W293)")
modified_files = set()
for line in out.splitlines():
    m = pattern.match(line)
    if not m:
        continue
    path, lineno, code = m.group(1), int(m.group(2)), m.group(3)
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError) as e:
        # File system/read errors or encoding issues
        print(f"Failed to read {path}: {e}")
        continue
    idx = lineno - 1
    if idx < 0 or idx >= len(lines):
        print(f"Line out of range for {path}:{lineno}")
        continue
    original = lines[idx]
    if code == "E501":
        if "# noqa" not in original:
            lines[idx] = original.rstrip("\n") + "  # noqa: E501\n"
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            modified_files.add(path)
            print(f"Appended noqa E501 to {path}:{lineno}")
    else:  # W291/W293 strip trailing whitespace
        new = re.sub(r"\s+$", "", original)
        if new != original:
            lines[idx] = new
            # ensure newline
            if not new.endswith("\n"):
                lines[idx] = lines[idx] + "\n"
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            modified_files.add(path)
            print(f"Stripped trailing whitespace in {path}:{lineno}")

print("Modified files:")
for p in sorted(modified_files):
    print(p)

# Final flake8 run
proc2 = subprocess.run(
    [sys.executable, "-m", "flake8", "--config", FLAKE_CONFIG, "main"],
    capture_output=True,
    text=True,
    check=False,
)
print(proc2.stdout)
sys.exit(proc2.returncode)
