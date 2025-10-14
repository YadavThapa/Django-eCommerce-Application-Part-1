"""Find distinct Product.image references in the DB and report missing files.

Intended to be run from the repository root. It ensures the project root is on
sys.path and then boots Django to access the ORM.
"""

import os
import sys

import django

# Ensure project root is on sys.path so imports like 'main' and 'shop' resolve
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure Django before importing ORM helpers
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "main.ecommerce_project.settings",
)
django.setup()


def main() -> None:
    """Run the check: import Django internals after settings are configured.

    This isolates Django imports to runtime so module-level import ordering
    tools do not report violations.
    """

    from django.apps import apps
    from django.conf import settings

    Product = apps.get_model("shop", "Product")
    image_list = list(Product.objects.values_list("image", flat=True))
    image_list = [i for i in image_list if i]
    uniq = sorted(set(image_list))
    print("Total distinct image refs:", len(uniq))

    missing = []
    for image in uniq:
        path = os.path.join(settings.MEDIA_ROOT, image)
        exists = os.path.exists(path)
        print(image, "->", "OK" if exists else "MISSING")
        if not exists:
            missing.append(image)

    print("MISSING COUNT:", len(missing))
    if missing:
        print("\nMissing examples:")
        for m in missing[:20]:
            print(" -", m)


if __name__ == "__main__":
    main()
