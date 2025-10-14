"""Django forms for the ecommerce shop application.

This module contains all form classes used in the shop application,
including user registration, profile management, product management,
store management, reviews, and checkout forms.
"""

from __future__ import annotations

import logging

from django import forms  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from .models import (
    Category,
    Product,
    Profile,
    Review,
    Store,
)

# Resolve the User model after imports to avoid executable code between imports
User = get_user_model()

# Many linters and static type checkers report false-positives when
# interacting with Django model managers and generated attributes like
# `.objects` and `DoesNotExist`. Silence those `no-member` warnings here
# for this forms module where model access is intentional.
# pylint: disable=no-member


# Module logger for debug tracing
logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with email, profile fields, and roles.

    This form extends Django's UserCreationForm to include additional fields
    for creating a complete user profile with role-based permissions.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        """Meta configuration for CustomUserCreationForm."""

        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """Initialize form with Bootstrap CSS classes for all fields."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        """Save user and create associated profile with role and info."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Debug: inspect any existing profile before updating
            try:
                existing = Profile.objects.get(user=user)
                logger.debug(
                    "Existing profile before update: user=%s role=%s",
                    user.pk,
                    getattr(existing, "role", None),
                )
            except Profile.DoesNotExist:
                existing = None
                logger.debug("No existing profile found for user=%s", user.pk)
            # Ensure profile is created/updated atomically so role cannot be
            # overwritten by other post_save signal handlers. Use
            # update_or_create to persist the chosen role and contact info.
            profile_obj, _ = Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": self.cleaned_data.get("role", "buyer"),
                    "phone": self.cleaned_data.get("phone", ""),
                    "address": self.cleaned_data.get("address", ""),
                },
            )

            # Ensure the in-memory user instance has the updated profile
            try:
                user.profile = profile_obj
            except (AttributeError, Profile.DoesNotExist):
                # Fallback: refresh user from DB and attach profile
                try:
                    user.refresh_from_db()
                    user.profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    # Profile still missing: allow test/assert to surface
                    # this situation rather than silently swallowing it.
                    pass

            # Debug: inspect profile after update
            try:
                updated = Profile.objects.get(user=user)
                logger.debug(
                    "Profile after update: user=%s role=%s",
                    user.pk,
                    getattr(updated, "role", None),
                )
            except Profile.DoesNotExist:
                logger.debug(
                    "Profile still does not exist after update for user=%s",
                    user.pk,
                )
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information and contact details."""

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        """Meta configuration for ProfileUpdateForm."""

        model = Profile
        fields = ["phone", "address"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with user data and Bootstrap CSS classes."""
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email
        # Add CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        """Save profile and update associated user information."""
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data["first_name"]
            self.user.last_name = self.cleaned_data["last_name"]
            self.user.email = self.cleaned_data["email"]
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class StoreForm(forms.ModelForm):
    """Form for creating and updating store information and branding."""

    class Meta:
        """Meta configuration for StoreForm."""

        model = Store
        fields = ["name", "description", "logo"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            if field == "logo":
                self.fields[field].widget.attrs.update({"class": "form-control-file"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class ProductForm(forms.ModelForm):
    """Form for creating and updating product listings and details."""

    class Meta:
        """Meta configuration for ProductForm."""

        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "quantity",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            if field == "image":
                self.fields[field].widget.attrs.update({"class": "form-control-file"})
            elif field == "category":
                self.fields[field].widget.attrs.update({"class": "form-select"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control"})
        # Make category not required
        self.fields["category"].required = False


class ReviewForm(forms.ModelForm):
    """Form for creating and submitting product reviews and ratings."""

    class Meta:
        """Meta configuration for ReviewForm."""

        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form and make comment field required."""
        super().__init__(*args, **kwargs)
        self.fields["comment"].required = True


class CategoryForm(forms.ModelForm):
    """Form for creating and managing product categories."""

    class Meta:
        """Meta configuration for CategoryForm."""

        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class CheckoutForm(forms.Form):
    """Form for collecting shipping and guest info during checkout."""

    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Enter your full name (required for guests)",
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text="Enter your email address (required for guests)",
    )
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        help_text="Enter your complete shipping address",
    )

    def __init__(self, *args, **kwargs):
        """Initialize form and pre-fill with user's address if available."""
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, "profile") and user.profile.address:
            self.fields["shipping_address"].initial = user.profile.address
        if user and user.is_authenticated:
            self.fields["name"].initial = f"{user.first_name} {user.last_name}".strip()
            self.fields["email"].initial = user.email


class PasswordResetRequestForm(forms.Form):
    """Form for requesting password reset via email address."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text="Enter the email address associated with your account",
    )

    def clean_email(self):
        """Validate that email address is associated with existing user."""
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email address.")
        return email


class PasswordResetForm(forms.Form):
    """Form for resetting password using a secure token."""

    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=8,
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=8,
    )

    def clean(self):
        """Validate that both password fields match."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ContactForm(forms.Form):
    """Contact form for customer support and inquiries."""

    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    subject = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "class": "form-control"})
    )
