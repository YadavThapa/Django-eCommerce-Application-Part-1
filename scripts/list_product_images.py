from django.conf import settings
from django.apps import apps
import os

Product = apps.get_model("shop", "Product")
seen = set()
missing = []
print("MEDIA_ROOT=", settings.MEDIA_ROOT)
for p in Product.objects.all():
    img = getattr(p, "image", None) or ""
    name = ""
    if hasattr(img, "name"):
        name = img.name
    else:
        name = str(img)
    if name in ("", "None"):
        continue
    path = name if os.path.isabs(name) else os.path.join(settings.MEDIA_ROOT, name)
    exists = os.path.exists(path)
    print(p.pk, name, "exists=", exists)
    if not exists and name not in seen:
        missing.append(name)
        seen.add(name)

print("\nMissing files:")
for m in missing:
    print(m)
