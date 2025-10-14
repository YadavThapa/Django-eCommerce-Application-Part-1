"""Small helper: print the tail of a file and its last raw bytes.

Used while debugging trailing-newline and EOF byte issues in tests.
"""

from pathlib import Path

p = Path("tests/integration/test_real_functionality.py")
text = p.read_text(encoding="utf8")
lines = text.splitlines()

for i, line in enumerate(lines[-30:], start=len(lines) - 29):
    print(f"{i:03d}:|{line}| (len={len(line)})")

print("--- EOF bytes ---")
print(text.encode("utf8")[-50:])
