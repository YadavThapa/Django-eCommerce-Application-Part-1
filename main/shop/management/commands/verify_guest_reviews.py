from django.core.management.base import BaseCommand
from django.db import transaction, DatabaseError

from main.shop.models import Review, OrderItem


class Command(BaseCommand):
    help = (
        "Retroactively mark unverified reviews as verified when a matching "
        "purchase exists (order buyer or guest_email). Use --dry-run to preview."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            help="Do not persist changes; only print what would be updated.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Stop after marking N reviews (0 = no limit).",
        )
        parser.add_argument(
            "--yes",
            action="store_true",
            dest="yes",
            help="Confirm performing changes (required to run without --dry-run).",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run")
        limit = int(options.get("limit") or 0)
        yes = options.get("yes")

        if not dry_run and not yes:
            self.stdout.write(
                (
                    "This command will modify Review records. Re-run with --yes to "
                    "apply changes or use --dry-run to preview the updates."
                )
            )
            return

        qs = Review.objects.filter(is_verified=False).select_related("user", "product")
        total = qs.count()
        self.stdout.write(f"Scanning {total} unverified reviews...")

        matched = 0
        updated = 0

        for review in qs.iterator():
            if limit and matched >= limit:
                break

            user = getattr(review, "user", None)
            user_email = getattr(user, "email", None) if user else None

            # Check buyer match or guest_email match. Database operations can
            # raise DatabaseError (connection issues, timeouts) which we catch
            # and continue scanning other reviews.
            try:
                purchased = False
                if user is not None:
                    purchased = OrderItem.objects.filter(
                        product=review.product, order__buyer=user
                    ).exists()
                if not purchased and user_email:
                    purchased = OrderItem.objects.filter(
                        product=review.product, order__guest_email__iexact=user_email
                    ).exists()
            except DatabaseError as exc:  # pragma: no cover - defensive
                self.stderr.write(
                    f"Database error checking orders for review {review.pk}: {exc}"
                )
                continue

            if purchased:
                matched += 1
                self.stdout.write(
                    f"Matched review {review.pk} (user={user_email}) -> set verified"
                )
                if not dry_run:
                    try:
                        with transaction.atomic():
                            review.is_verified = True
                            review.save(update_fields=["is_verified"])
                            updated += 1
                    except DatabaseError as exc:  # pragma: no cover - defensive
                        # Only catch database-related errors here; other
                        # unexpected errors should surface to the caller.
                        self.stderr.write(f"Failed to update review {review.pk}: {exc}")

        self.stdout.write(f"Done. matched={matched} updated={(updated if not dry_run else 0)}")
