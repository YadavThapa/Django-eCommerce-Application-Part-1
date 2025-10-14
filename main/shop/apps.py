"""Django app configuration for the shop application."""

from django.apps import AppConfig  # type: ignore


class ShopConfig(AppConfig):
    """Configuration for the shop Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"
