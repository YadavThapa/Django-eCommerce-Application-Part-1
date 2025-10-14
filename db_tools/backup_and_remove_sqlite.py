"""Backup and remove the project's SQLite file safely.

Copied into db_tools/ for centralized DB utilities.
"""

import os
import shutil
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "db.sqlite3")
backdir = os.path.join(ROOT, "backups")

if not os.path.exists(src):
    print("ERROR: source file not found:", src)
    raise SystemExit(2)

os.makedirs(backdir, exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
dst = os.path.join(backdir, f"db_sqlite_backup_{stamp}.sqlite3")

try:
    shutil.copy2(src, dst)
    print("BACKUP_CREATED:", dst)
except Exception as e:
    print("ERROR during copy:", e)
    raise SystemExit(3) from e

try:
    os.remove(src)
    print("SOURCE_DELETED:", src)
except Exception as e:
    print("ERROR deleting source:", e)
    raise SystemExit(4) from e

# list backups
backups = sorted([f for f in os.listdir(backdir) if f.startswith("db_sqlite_backup_")])
print("BACKUPS_IN_DIR:")
for b in backups:
    path = os.path.join(backdir, b)
    size = os.path.getsize(path)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
    print(path, size, mtime)

print("DONE")
