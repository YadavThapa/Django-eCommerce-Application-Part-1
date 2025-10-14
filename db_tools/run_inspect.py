"""Run quick inspection of DB and a few Product image paths.

This script lives in `db_tools/` to centralize DB-related utilities.
Run via the wrapper in `scripts/` to preserve previous invocation paths, or
run directly from the repository root.
"""

# Allow imports that happen after sys.path manipulation and Django setup.
# pylint: disable=import-outside-toplevel

import os
import sys

# repo root is parent directory of db_tools/
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if os.path.join(project_root, "main") not in sys.path:
    sys.path.insert(0, os.path.join(project_root, "main"))


def main() -> None:
    """Perform runtime inspections using Django ORM.

    Django imports and setup are done inside main() so the module can be
    imported without side-effects and linters don't complain about
    import ordering.
    """

    # Configure Django for the project and make ORM usable.
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
    django.setup()

    # Local imports that depend on Django being configured
    from django.apps import apps  # noqa: E402
    from django.conf import settings  # noqa: E402
    from django.contrib.auth import get_user_model  # noqa: E402
    from django.db import connection  # noqa: E402

    print("ACTIVE DB ENGINE:", connection.settings_dict.get("ENGINE"))
    print("DB NAME:", connection.settings_dict.get("NAME"))

    tables = list(connection.introspection.table_names())
    print("\nTABLES SAMPLE:", tables[:40])

    user_model = get_user_model()
    try:
        print("\nauth_user count =", user_model.objects.count())
    except RuntimeError as exc:
        print("Could not count auth_user:", type(exc).__name__, exc)

    for app_label, model_name in (
        ("shop", "Product"),
        ("shop", "Order"),
        ("shop", "Cart"),
    ):
        model_cls = apps.get_model(app_label, model_name)
        if model_cls is None:
            print(f"Model {app_label}.{model_name} not installed")
            continue

        try:
            print(f"{app_label}.{model_name} count =", model_cls.objects.count())
        except RuntimeError as exc:
            print(f"Could not count {app_label}.{model_name}:", type(exc).__name__, exc)

    # Check media files for a few products
    print("\nMEDIA_ROOT:", getattr(settings, "MEDIA_ROOT", None))
    try:
        product_model = apps.get_model("shop", "Product")
        products = product_model.objects.all()[:5]
        print("Sample products:")
        for p in products:
            # Attempt to read a common image field or image URL attribute
            img_path = None
            if hasattr(p, "image") and p.image:
                img_path = p.image.path if hasattr(p.image, "path") else str(p.image)
            elif hasattr(p, "images"):
                # some projects use related images; attempt to fetch first
                try:
                    img_qs = p.images.all()
                    if img_qs:
                        first = img_qs[0]
                        img_path = getattr(first, "image", None) or getattr(
                            first, "file", None
                        )
                except RuntimeError:
                    img_path = None

            print(" -", getattr(p, "name", str(p)), "| id=", p.pk, "| image=", img_path)
            if img_path:
                # if it's a path relative to MEDIA_ROOT, check existence
                candidate = img_path
                if not os.path.isabs(candidate) and settings.MEDIA_ROOT:
                    candidate = os.path.join(settings.MEDIA_ROOT, candidate)
                print("   exists:", os.path.exists(candidate))
    except RuntimeError as exc:
        print("Could not inspect product images:", type(exc).__name__, exc)

    # Check for sqlite file and backups
    print(
        "\ndb.sqlite3 exists?", os.path.exists(os.path.join(project_root, "db.sqlite3"))
    )
    backup_dir = os.path.join(project_root, "backups")
    if os.path.isdir(backup_dir):
        backups = [f for f in os.listdir(backup_dir) if f.startswith("sqlite_migrate")]
        print("Found sqlite backups:", backups)
    else:
        print("No backups directory found")


if __name__ == "__main__":
    main()
