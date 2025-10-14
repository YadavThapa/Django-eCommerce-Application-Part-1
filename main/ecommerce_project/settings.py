"""Project settings for the Django E-commerce application.

This module contains runtime configuration used by `manage.py` and the
WSGI/ASGI entry points. Imports are grouped at the top to satisfy linters
while keeping behavior identical to the previous file.
"""

import os
from pathlib import Path


# After moving the project into `main/`, make BASE_DIR point to the
# repository root so paths like db.sqlite3, static/ and media/ remain
# unchanged.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# NOTE: keep secret key as-is for development; in production inject via env
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


# Database configuration: default to Postgres (persistent local container).
# You can still override via environment variables. To use SQLite set
# DB_ENGINE=sqlite.
DB_ENGINE = os.environ.get("DB_ENGINE", "postgres").lower()
DB_NAME = os.environ.get("DB_NAME", "ecommerce_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "15433")

if DB_ENGINE in ("mysql", "mariadb"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT or "3306",
            "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "0")),
        }
    }
elif DB_ENGINE in ("postgres", "postgresql", "psycopg2"):
    # Configure PostgreSQL when DB_ENGINE indicates a postgres backend.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT or "5432",
        }
    }
elif DB_ENGINE in ("postgres", "postgresql", "psycopg2"):
    # Configure PostgreSQL when DB_ENGINE indicates a postgres backend.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT or "5432",
        }
    }
else:
    # Fallback to SQLite if explicitly requested via DB_ENGINE=sqlite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Use DB sessions
# Use compact application serializer in shop.utils
SESSION_SERIALIZER = "shop.utils.serializers.PickleSerializer"

# Cart session settings
CART_SESSION_ID = "cart"

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # For development
DEFAULT_FROM_EMAIL = "noreply@himalayanecommerce.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""  # Add your email here for production
EMAIL_HOST_PASSWORD = ""  # Add your password here for production

# For production, set the SMTP backend, e.g:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Authentication URLs
LOGIN_REDIRECT_URL = "/profile/"
LOGOUT_REDIRECT_URL = "/"
