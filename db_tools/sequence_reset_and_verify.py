"""Reset Postgres sequences after data load and print verification info.

Copied into db_tools/ to centralize Postgres-and-database helper scripts.
"""

import os
import sys
import django

from django.apps import apps
from django.conf import settings
from django.db import connection


def main() -> None:
    """Reset Postgres sequences for common apps and print verification."""

    # Ensure project root and main on path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    if os.path.join(project_root, "main") not in sys.path:
        sys.path.insert(0, os.path.join(project_root, "main"))

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "main.ecommerce_project.settings",
    )
    django.setup()

    print("Using DB:", connection.settings_dict.get("ENGINE"))
    print("DB NAME:", connection.settings_dict.get("NAME"))

    # Reset sequences for models in auth and shop apps
    apps_to_fix = ["auth", "shop"]
    with connection.cursor() as cursor:
        for app_label in apps_to_fix:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                table = model._meta.db_table  # pylint: disable=protected-access
                pk_col = model._meta.pk.column  # pylint: disable=protected-access
                try:
                    sql_query = f"SELECT COALESCE(MAX({pk_col}), 0) FROM {table}"
                    cursor.execute(sql_query)
                    max_id = cursor.fetchone()[0] or 0
                    if max_id > 0:
                        seq_value = max_id
                        seq_is_called = "true"
                    else:
                        seq_value = 1
                        seq_is_called = "false"

                    seq_sql_cmd = (
                        f"SELECT setval(pg_get_serial_sequence('{table}','{pk_col}'), "
                        f"{seq_value}, {seq_is_called});"
                    )
                    cursor.execute(seq_sql_cmd)
                    print(
                        f"Reset sequence for {table} to {seq_value} (is_called={seq_is_called})"
                    )
                except RuntimeError as exc:
                    print(f"Skipping sequence reset for {table}:", exc)


def print_count_for(app_label_arg: str, model_name_arg: str) -> None:
    """Print the object count for the given model if available."""

    model_cls = apps.get_model(app_label_arg, model_name_arg)
    if model_cls is None:
        print(f"Model {app_label_arg}.{model_name_arg} not installed")
        return

    try:
        cnt = model_cls.objects.count()
        print(f"{app_label_arg}.{model_name_arg} count =", cnt)
    except RuntimeError as exc:
        print(f"Could not count {app_label_arg}.{model_name_arg}:", exc)

    # Print sample products and their image files
    print_count_for("auth", "User")
    print_count_for("shop", "Product")
    print_count_for("shop", "Order")
    print_count_for("shop", "Cart")

    print("\nMEDIA_ROOT =", getattr(settings, "MEDIA_ROOT", None))
    product_model = apps.get_model("shop", "Product")
    if product_model is not None:
        for p in product_model.objects.all()[:10]:
            image_path = None
            if hasattr(p, "image") and p.image:
                try:
                    if hasattr(p.image, "path"):
                        image_path = p.image.path
                    else:
                        image_path = str(p.image)
                except AttributeError:
                    image_path = str(p.image)

            print(f"Product {p.pk} {getattr(p, 'name', '')} image -> {image_path}")
            if image_path and settings.MEDIA_ROOT:
                candidate = image_path
                if not os.path.isabs(candidate):
                    candidate = os.path.join(settings.MEDIA_ROOT, candidate)
                print("  exists:", os.path.exists(candidate))
    else:
        print("No Product model available; skipping sample list")

    print("\nDone")


if __name__ == "__main__":
    main()
