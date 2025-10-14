import logging
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from shop.models import Product

logger = logging.getLogger(__name__)

# Mapping heuristics mirroring the templatetag. Tuples are
# (predicate, filename) where filename may be None meaning no match.
HEURISTICS = [
    (lambda n: "headphone" in n or "headphones" in n, None),
    (
        lambda n: any(
            k in n
            for k in (
                "smartphone",
                "phone",
                "mobile",
                "iphone",
                "samsung",
            )
        ),
        None,
    ),
    (lambda n: any(k in n for k in ("laptop", "computer", "macbook")), None),
    (
        lambda n: any(k in n for k in ("running", "shoe", "shoes")),
        "running_shoes.jpg",
    ),
    (lambda n: "dumbbell" in n or "dumbbells" in n, "dumbbells_set.jpg"),
    (lambda n: "yoga" in n and "mat" in n, "yoga_mat.jpg"),
    (lambda n: "tennis" in n and "racket" in n, "tennis_racket.jpg"),
    (lambda n: "basketball" in n, "basketball.jpg"),
    (lambda n: "football" in n and "american" not in n, "football.jpg"),
    (
        lambda n: "cooking" in n and "masterclass" in n,
        "cooking_masterclass.jpg",
    ),
    (lambda n: "history" in n and "nepal" in n, "history_of_nepal.jpg"),
]

STATIC_PRODUCTS_DIR = Path(settings.BASE_DIR) / "static" / "img" / "products"
MEDIA_PRODUCTS_DIR = Path(settings.MEDIA_ROOT) / "product_images"


class Command(BaseCommand):
    """Attach curated static product images into MEDIA and assign them.

    The command runs as a dry-run unless --apply is provided.
    This command uses getattr() when referencing `self.style` members so
    static analyzers (pylint) that can't see Django's runtime-provided
    members don't raise false positives.
    """

    help = (
        "Attach curated static product images into MEDIA and assign to "
        "products that lack images or have placeholders."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Actually copy files and assign images.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=("Show proposed changes but do not modify files or DB."),
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        dry_run = options["dry_run"] or not apply_changes

        # Use getattr to avoid pylint false-positives about `style` members
        def _styled(name, message):
            styler = getattr(self, "style", None)
            if styler is None:
                return message
            member = getattr(styler, name, None)
            if callable(member):
                return member(message)
            return message

        if dry_run:
            self.stdout.write(
                _styled(
                    "WARNING",
                    "Running in dry-run mode. No changes will be made.",
                )
            )
        else:
            self.stdout.write(
                _styled(
                    "SUCCESS",
                    "Applying changes: copying files and assigning images.",
                )
            )

        MEDIA_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

        qs = Product.objects.all()
        changed = []

        for p in qs:
            name = (p.name or "").lower()
            img_name = getattr(p.image, "name", "") or ""
            needs = False
            if not img_name or "product_placeholder" in img_name:
                needs = True

            if not needs:
                continue

            # pick heuristic
            chosen = None
            for check, filename in HEURISTICS:
                try:
                    if check(name):
                        chosen = filename
                        break
                # pylint: disable=broad-exception-caught
                except Exception as exc:  # pragma: no cover - defensive
                    # Defensive: heuristic lambdas may raise unexpected
                    # exceptions (e.g. from custom predicates). Narrowly
                    # re-raise system-exiting exceptions and log others.
                    if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                        raise
                    # pylint: disable=broad-exception-caught
                    logger.exception("Heuristic failed for %s: %s", name, exc)
                    continue

            if not chosen:
                chosen = "product_default.jpg"

            src = STATIC_PRODUCTS_DIR / chosen
            if not src.exists():
                self.stdout.write(
                    _styled(
                        "ERROR",
                        f"Missing static image {src} for product {p.name}. "
                        "Skipping.",
                    )
                )
                continue

            dest_filename = f"{p.pk}_{chosen}"
            dest_path = MEDIA_PRODUCTS_DIR / dest_filename

            changed.append((p, src, dest_path))
            if dry_run:
                self.stdout.write(
                    f"Would assign {src.name} -> {dest_path.name} "
                    f"for product {p.pk} - {p.name}"
                )
            else:
                # copy and assign using Path operations
                dest_path.write_bytes(src.read_bytes())
                rel_path = os.path.join("product_images", dest_filename)
                p.image.name = rel_path
                p.save()
                self.stdout.write(
                    _styled(
                        "SUCCESS",
                        f"Assigned {rel_path} to product {p.pk} - {p.name}",
                    )
                )

        self.stdout.write(_styled("NOTICE", f"Processed {len(changed)} products."))
