"""Small utility to inspect the active Django DB connection and a few tables.

This was moved into db_tools/ to centralize DB-related developer utilities.
Use the wrapper in `scripts/` or run this file directly from the repository root.
"""

import glob
import os

from django.apps import apps
from django.contrib.auth import get_user_model  # type: ignore
from django.db import connection

# Resolve user model after imports to avoid module-level code between imports
User = get_user_model()


print("ENGINE=", connection.settings_dict.get("ENGINE"))
print("NAME=", connection.settings_dict.get("NAME"))
print("\nTABLES SAMPLE:", list(connection.introspection.table_names())[:40])


print("auth_user count =", User.objects.count())

# Check counts for a few shop models if available
for app_label, model_name in (
    ("shop", "Order"),
    ("shop", "Cart"),
    ("shop", "Product"),
):
    Model = apps.get_model(app_label, model_name)
    if Model is None:
        print(f"Model {app_label}.{model_name} not installed")
        continue

    try:
        print(f"{app_label}.{model_name} count =", Model.objects.count())
    except RuntimeError as exc:
        # RuntimeError can occur if DB connection is not ready.
        print(
            f"Could not count {app_label}.{model_name}: {type(exc).__name__}:",
            exc,
        )


print("\ndb.sqlite3 exists?", os.path.exists("db.sqlite3"))
print("sqlite backups:", glob.glob("backups/sqlite_migrate*.db"))
