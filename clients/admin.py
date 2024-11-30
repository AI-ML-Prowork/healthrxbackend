"""
Admin interface configuration for the `UserProfile` and `Blog` models.

This module registers custom admin interfaces for the `UserProfile` and `Blog` models. It specifies how these models are displayed and managed in the Django admin site.

Models Registered:
- `UserProfile`: Provides admin interface configuration for user profiles.
- `Blog`: Provides admin interface configuration for blog entries.

Admin Classes:
- `UserProfileAdmin`:
    - Custom admin interface for the `UserProfile` model.
    - Displays the `user` field in the list view.

- `BlogAdmin`:
    - Custom admin interface for the `Blog` model.
    - Displays the `title` and `description` fields in the list view.

Usage:
- The `UserProfile` model admin interface is registered with the Django admin site to display user profile information.
- The `Blog` model admin interface is registered with the Django admin site to display blog entries.

Note:
- Both models use the `OrganizationAdmin` class, which should be renamed to reflect the specific model being configured for clarity.

"""

from django.contrib import admin
from .models import UserProfile, Blog


@admin.register(UserProfile)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Blog)
class OrganizationAdminBlog(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
