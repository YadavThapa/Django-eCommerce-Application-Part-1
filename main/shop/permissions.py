"""
Authentication and permission decorators for role-based access control.

This module provides decorators and a CBV mixin used across the project to
gate access by role, group, and Django permissions. The implementation is
intended to be behavior-preserving; edits here only adjust formatting and
small refactors to satisfy linters.
"""

# When an editor runs linters outside the project's venv it may report
# import-error for Django modules. Suppress import-error here only; this is
# non-functional and safe to remove once the proper interpreter is selected.
# pylint: disable=import-error

from functools import wraps

from django.contrib import messages  # type: ignore

# Django imports: silence type-checker warnings when stubs are not present
from django.contrib.auth.decorators import login_required  # type: ignore
from django.core.exceptions import PermissionDenied  # type: ignore
from django.http import Http404, HttpResponseForbidden  # type: ignore
from django.shortcuts import redirect, render  # type: ignore

# Reference these low-level symbols so linters don't mark them unused.
# They are re-exported by the root-level compatibility shim.
_REEXPORTS = (PermissionDenied, HttpResponseForbidden, render)


def role_required(allowed_roles):
    """Require the user to have one of the allowed roles.

    allowed_roles should be an iterable of role names (strings).
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, "profile") or not request.user.profile:
                messages.error(request, "Access denied. Profile not found.")
                return redirect("shop:home")

            user_role = request.user.profile.role
            if user_role not in allowed_roles:
                allowed_text = ", ".join(allowed_roles)
                msg = (
                    "Access denied. This page is restricted to "
                    f"{allowed_text} users only."
                )
                messages.error(request, msg)
                return redirect("shop:home")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def admin_required(view_func):
    """Require admin (staff or superuser) access for the view."""

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            msg = "Access denied. Admin privileges required."
            messages.error(request, msg)
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def staff_required(view_func):
    """Require staff access for the view."""

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            msg = "Access denied. Staff privileges required."
            messages.error(request, msg)
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def superuser_required(view_func):
    """Require superuser access for the view."""

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            msg = "Access denied. Superuser privileges required."
            messages.error(request, msg)
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def vendor_required(view_func):
    """Require vendor role for the view."""

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if (
            not hasattr(request.user, "profile")
            or not request.user.profile
            or request.user.profile.role != "vendor"
        ):
            msg = "Access denied. Vendor account required."
            messages.error(request, msg)
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def buyer_required(view_func):
    """Require buyer role for the view."""

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if (
            not hasattr(request.user, "profile")
            or not request.user.profile
            or request.user.profile.role != "buyer"
        ):
            # Do not show a hard-coded alert message here; keep the
            # redirect behavior but avoid surfacing this specific
            # message to the user interface.
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def anonymous_required(view_func):
    """Only allow access to anonymous (not authenticated) users."""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("shop:home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def owner_required(model_class, pk_field="pk", user_field="user"):
    """Allow access only to the owner of a given model instance.

    Nested user lookups (e.g. 'store__vendor') are supported via "__".
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Import at runtime to avoid top-level Django imports; silence
            # pylint's import-outside-toplevel warning for this deliberate
            # pattern.
            # pylint: disable=import-outside-toplevel
            from django.shortcuts import get_object_or_404  # type: ignore

            # pylint: enable=import-outside-toplevel

            obj_id = kwargs.get(pk_field)
            if not obj_id:
                messages.error(request, "Object ID not found.")
                return redirect("shop:home")

            try:
                if "__" in user_field:
                    filter_dict = {user_field: request.user}
                    filter_kwargs = {pk_field: obj_id}
                    filter_kwargs.update(filter_dict)
                    obj = get_object_or_404(model_class, **filter_kwargs)
                else:
                    obj = get_object_or_404(model_class, **{pk_field: obj_id})
                    if getattr(obj, user_field) != request.user:
                        msg = "Access denied. You do not own this resource."
                        messages.error(request, msg)
                        return redirect("shop:home")

                kwargs["object"] = obj

            except (AttributeError, Http404):
                # Narrow exceptions to attribute access issues or a missing
                # object (get_object_or_404 raises Http404). This avoids
                # catching unrelated exceptions while preserving the
                # original behavior of redirecting on not-found/access-denied.
                messages.error(request, "Resource not found or access denied.")
                return redirect("shop:home")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def group_required(*group_names):
    """Require membership in at least one of the supplied Django groups."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=group_names).exists():
                groups_text = ", ".join(group_names)
                msg = (
                    f"Access denied. You must be in one of these groups: "
                    f"{groups_text}"
                )
                messages.error(request, msg)
                return redirect("shop:home")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def permission_required(permission_name):
    """Require a specific Django permission for the view."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(permission_name):
                msg = f'Access denied. You need the "{permission_name}" ' "permission."
                messages.error(request, msg)
                return redirect("shop:home")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


class PermissionMixin:
    """Mixin for class-based views to perform permission and role checks."""

    required_roles = None
    required_permissions = None
    required_groups = None
    admin_required = False
    staff_required = False
    superuser_required = False

    def dispatch(self, request, *args, **kwargs):
        """Enforce authentication and configured role/permission/group checks.

        This method performs the same redirects and messages as the
        function-based decorators above. It returns the superclass
        dispatch when all checks pass.
        """

        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect("shop:login")

        if self.superuser_required and not request.user.is_superuser:
            msg = "Access denied. Superuser privileges required."
            messages.error(request, msg)
            return redirect("shop:home")

        if self.admin_required and not (
            request.user.is_staff or request.user.is_superuser
        ):
            msg = "Access denied. Admin privileges required."
            messages.error(request, msg)
            return redirect("shop:home")

        if self.staff_required and not request.user.is_staff:
            msg = "Access denied. Staff privileges required."
            messages.error(request, msg)
            return redirect("shop:home")

        if self.required_roles:
            if (
                not hasattr(request.user, "profile")
                or not request.user.profile
                or request.user.profile.role not in self.required_roles
            ):
                roles_text = ", ".join(self.required_roles)
                msg = (
                    f"Access denied. This page is restricted to {roles_text} "
                    "users only."
                )
                messages.error(request, msg)
                return redirect("shop:home")

        if self.required_permissions:
            for permission in self.required_permissions:
                if not request.user.has_perm(permission):
                    msg = f'Access denied. You need the "{permission}" ' "permission."
                    messages.error(request, msg)
                    return redirect("shop:home")

        if self.required_groups:
            if not request.user.groups.filter(name__in=self.required_groups).exists():
                groups_text = ", ".join(self.required_groups)
                msg = (
                    "Access denied. You must be in one of these groups: "
                    f"{groups_text}"
                )
                messages.error(request, msg)
                return redirect("shop:home")

        return super().dispatch(request, *args, **kwargs)


def api_permission_required(allowed_roles=None, admin_only=False):
    """Decorator for API views returning JSON error responses.

    Returns JSON responses for denied access so API callers get structured
    error objects rather than redirects.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Import at runtime to avoid top-level Django imports; silence
            # pylint's import-outside-toplevel warning for this deliberate
            # pattern.
            # pylint: disable=import-outside-toplevel
            from django.http import JsonResponse  # type: ignore

            # pylint: enable=import-outside-toplevel

            if not request.user.is_authenticated:
                return JsonResponse(
                    {
                        "error": "Authentication required",
                        "detail": ("You must be logged in to access this endpoint."),
                    },
                    status=401,
                )

            if admin_only and not (request.user.is_staff or request.user.is_superuser):
                return JsonResponse(
                    {
                        "error": "Admin privileges required",
                        "detail": "This endpoint requires admin access.",
                    },
                    status=403,
                )

            if allowed_roles:
                if (
                    not hasattr(request.user, "profile")
                    or not request.user.profile
                    or request.user.profile.role not in allowed_roles
                ):
                    allowed_text = ", ".join(allowed_roles)
                    return JsonResponse(
                        {
                            "error": "Insufficient privileges",
                            "detail": (
                                f"This endpoint is restricted to "
                                f"{allowed_text} users."
                            ),
                        },
                        status=403,
                    )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


# Utility functions for templates and other checks
def user_has_role(user, role):
    """Return True if the authenticated user has the given role."""
    if not user.is_authenticated:
        return False
    if not hasattr(user, "profile") or not user.profile:
        return False
    return user.profile.role == role


def user_is_vendor(user):
    """Return True when the given user has the vendor role."""
    return user_has_role(user, "vendor")


def user_is_buyer(user):
    """Return True when the given user has the buyer role."""
    return user_has_role(user, "buyer")


def user_is_admin(user):
    """Return True when the user is authenticated and has admin rights.

    Admin rights are defined as staff or superuser status.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def user_can_access_admin(user):
    """Return True if the authenticated user is staff (can access admin)."""
    return user.is_authenticated and user.is_staff


def user_owns_object(user, obj, user_field="user"):
    """Return True if user owns the given object; supports nested lookups."""
    if not user.is_authenticated:
        return False
    try:
        if "__" in user_field:
            fields = user_field.split("__")
            current_obj = obj
            for field in fields:
                current_obj = getattr(current_obj, field)
            return current_obj == user
        else:
            return getattr(obj, user_field) == user
    except AttributeError:
        return False
