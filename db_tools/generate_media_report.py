"""Generate a CSV verifying product image filesystem presence.

Copied into db_tools/ to centralize DB/media inspection utilities.
"""

from pathlib import Path
import csv
import os
import sys

# It's acceptable to import Django at module import time; calling
# ``django.setup()`` happens inside main() after we ensure the
# environment and sys.path are configured. This ordering keeps imports
# at the top (satisfying linters) while deferring setup until runtime.
import django
from django.apps import apps
from django.conf import settings


def main() -> None:
    """Configure Django and generate a CSV verifying product images.

    This function mirrors the previous top-level script behavior but is
    wrapped so linters don't complain about module-level runtime code.
    """

    # Ensure repo root and main/ are importable (same as manage.py)
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "main"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
    # Ensure DB env uses the persistent Postgres container
    os.environ.setdefault("DB_ENGINE", "postgres")
    os.environ.setdefault("DB_NAME", "ecommerce_db")
    os.environ.setdefault("DB_USER", "postgres")
    os.environ.setdefault("DB_PASSWORD", "postgres")
    os.environ.setdefault("DB_HOST", "127.0.0.1")
    os.environ.setdefault("DB_PORT", "15433")

    # Configure Django now that environment and sys.path are ready
    django.setup()

    product_model = apps.get_model("shop", "Product")

    out_dir = root / "backups"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "media_verification.csv"

    with out_file.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["product_id", "name", "image_field", "filesystem_path", "exists"]
        )
        for p in product_model.objects.all().order_by("pk"):
            img = getattr(p, "image", None) or ""
            if hasattr(img, "name"):
                name = img.name
            else:
                name = str(img)
            if not name or name in ("None", ""):
                fs_path = ""
                exists = False
            else:
                if os.path.isabs(name):
                    fs_path = name
                else:
                    fs_path = os.path.join(settings.MEDIA_ROOT, name)
                exists = os.path.exists(fs_path)
            writer.writerow([p.pk, getattr(p, "name", ""), name, fs_path, exists])

    # Print summary
    print("Wrote media report to", out_file)
    count_total = product_model.objects.count()
    count_missing = 0
    for prod in product_model.objects.all():
        img_name = getattr(prod.image, "name", str(prod.image))
        if not img_name:
            count_missing += 1
            continue
        if os.path.isabs(img_name):
            fs_path = img_name
        else:
            fs_path = os.path.join(settings.MEDIA_ROOT, img_name)
        if not os.path.exists(fs_path):
            count_missing += 1

    print("Total products =", count_total)
    print("Missing images =", count_missing)


if __name__ == "__main__":
    main()
