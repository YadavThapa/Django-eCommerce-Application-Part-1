"""Project settings for the Django E-commerce application.

This module intentionally contains runtime configuration and is used by
manage.py and the WSGI/ASGI entry points. The docstring here satisfies
linters that expect a module-level description.
"""

from pathlib import Path
import os

# BASE_DIR should point to the repository root so paths like db.sqlite3,
# static/ and media/ remain unchanged when the project lives at the
# repository top-level.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    "django-insecure-jr=hwpic(5y&a)d+@hdk^mma92thc!l0ijj)w+8)e)cfjq5)9c"  # noqa: E501
)

# Allow overriding debug and allowed hosts via environment for safer external testing.
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS can be set as a comma-separated env var, e.g. '*' or '127.0.0.1,localhost'
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap4",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shop_middleware.PermissionMiddleware",
    "shop_middleware.SecurityMiddleware",
    "shop_middleware.UserActivityMiddleware",
]

ROOT_URLCONF = "ecommerce_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.context_processors.auth_context",
                "shop.context_processors.permissions_context",
                "shop.context_processors.navigation_context",
                "shop.context_processors.breadcrumb_context",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce_project.wsgi.application"

# Database configuration: prefer PostgreSQL when environment variables are
# present, or when USE_POSTGRES is explicitly set. Otherwise fall back to
# SQLite.
USE_POSTGRES = os.environ.get("USE_POSTGRES", "False").lower() in (
    "1",
    "true",
    "yes",
)
POSTGRES_DB = os.environ.get("POSTGRES_DB")
if USE_POSTGRES or POSTGRES_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "postgres"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            # use a plain string for NAME so type-checkers expect str
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Session configuration for cart persistence
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep sessions when browser closes
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Use database sessions
# Use compact application serializer in shop.utils
SESSION_SERIALIZER = "shop.utils.serializers.PickleSerializer"

# Cart session settings
CART_SESSION_ID = "cart"

# Email configuration
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # For development  # noqa: E501
)
DEFAULT_FROM_EMAIL = "noreply@himalayanecommerce.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""  # Add your email here for production
EMAIL_HOST_PASSWORD = ""  # Add your password here for production

# For production, use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Authentication URLs
LOGIN_REDIRECT_URL = "/profile/"  # Redirect to profile page after login
LOGOUT_REDIRECT_URL = "/"  # Redirect to home page after logout
# Ensure Django redirects unauthenticated users to the project's login page
LOGIN_URL = "/login/"
