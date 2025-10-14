"""
Middleware for enhanced authentication and permission checking
moved into the `shop` package to group related code together.
"""

import logging

from django.contrib import messages  # type: ignore
from django.shortcuts import redirect  # type: ignore
from django.utils import timezone  # type: ignore
from django.utils.deprecation import MiddlewareMixin  # type: ignore

logger = logging.getLogger(__name__)


class PermissionMiddleware(MiddlewareMixin):
    """
    Middleware to enforce global permission rules and security measures
    """

    ROLE_PROTECTED_URLS = {
        "shop:vendor_dashboard": ["vendor"],
        "shop:store_list": ["vendor"],
        "shop:store_create": ["vendor"],
        "shop:vendor_products": ["vendor"],
        "shop:customer_dashboard": ["buyer"],
        "shop:order_history": ["buyer"],
        "shop:category_list": ["admin"],
        "shop:category_create": ["admin"],
    }

    ADMIN_PROTECTED_URLS = [
        "shop:category_list",
        "shop:category_create",
        "shop:category_update",
        "shop:category_delete",
    ]

    ANONYMOUS_ONLY_URLS = [
        "shop:login",
        "shop:register",
        "shop:password_reset_request",
        "shop:password_reset_confirm",
    ]

    def process_view(self, request, _view_func, _view_args, _view_kwargs):
        """Inspect the request before the view runs and enforce access rules.

        Returns None to continue request processing, or an HttpResponse
        (usually a redirect) when access is denied.
        """
        if request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return None

        current_url = None
        try:
            if hasattr(request, "resolver_match") and request.resolver_match:
                current_url = request.resolver_match.url_name
                if request.resolver_match.namespace:
                    current_url = f"{request.resolver_match.namespace}:{{current_url}}"
        except AttributeError:
            pass

        if not current_url:
            return None

        if current_url in self.ANONYMOUS_ONLY_URLS and request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("shop:home")

        if current_url in self.ADMIN_PROTECTED_URLS:
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect("shop:login")
            if not (request.user.is_staff or request.user.is_superuser):
                messages.error(
                    request,
                    "Access denied. Admin privileges required.",
                )
                return redirect("shop:home")

        if current_url in self.ROLE_PROTECTED_URLS:
            required_roles = self.ROLE_PROTECTED_URLS[current_url]
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect("shop:login")

            user_role = None
            if hasattr(request.user, "profile") and request.user.profile:
                user_role = request.user.profile.role

            if user_role not in required_roles:
                role_names = ", ".join(required_roles)
                # Use an f-string for clearer formatting
                messages.error(
                    request,
                    f"Access denied. This page is for {role_names}" " users only.",
                )
                return redirect("shop:home")

        return None


class SecurityMiddleware(MiddlewareMixin):
    """Additional security middleware for the e-commerce platform"""

    def process_request(self, request):
        """Inspect incoming requests for suspicious or malicious patterns.

        Logs warnings/errors and returns an HttpResponse redirect when
        malicious content is detected; otherwise returns None.
        """
        if self._is_suspicious_request(request):
            logger.warning(
                "Suspicious request detected: %s %s from %s",
                request.method,
                request.path,
                request.META.get("REMOTE_ADDR", "unknown"),
            )

        if self._has_sql_injection_patterns(request):
            logger.error(
                "Potential SQL injection attempt: %s from %s",
                request.path,
                request.META.get("REMOTE_ADDR", "unknown"),
            )
            messages.error(request, "Invalid request detected.")
            return redirect("shop:home")

        return None

    def _is_suspicious_request(self, request):
        suspicious_paths = [
            "/admin/login/",
            "/wp-admin/",
            "/phpmyadmin/",
            "/.env",
            "/config.php",
        ]
        return any(path in request.path.lower() for path in suspicious_paths)

    def _has_sql_injection_patterns(self, request):
        sql_patterns = [
            "union select",
            "drop table",
            "insert into",
            "delete from",
            "update set",
            "--",
            "/*",
            "xp_",
            "sp_",
        ]
        query_string = request.META.get("QUERY_STRING", "").lower()
        if any(pattern in query_string for pattern in sql_patterns):
            return True
        if hasattr(request, "POST"):
            post_data = str(request.POST).lower()
            if any(pattern in post_data for pattern in sql_patterns):
                return True
        return False


class UserActivityMiddleware(MiddlewareMixin):
    """Middleware to track user activity and enforce activity-based rules"""

    def process_response(self, request, _response):
        """Update authenticated user's last activity timestamp on response.

        Any exceptions are caught and logged; activity-tracking failures
        must not break the response flow.
        """
        if request.user.is_authenticated and hasattr(request.user, "profile"):
            try:
                if hasattr(request.user.profile, "last_activity"):
                    request.user.profile.last_activity = timezone.now()
                    request.user.profile.save(update_fields=["last_activity"])
            except Exception:  # pylint: disable=broad-except
                # Broad exception is intentional here: don't
                # activity-tracking failures break the request flow.
                # Log full traceback.
                logger.exception("Error updating user activity")
        return _response
