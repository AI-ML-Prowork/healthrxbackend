"""
This module defines custom admin interfaces for the application's models.

Custom Admin Classes:
1. `CustomUserAdmin`:
    - Extends `UserAdmin` to provide a customized admin interface for the `CustomUser` model.
    - Displays the following fields in the list view: `email`, `username`, `is_tenant_admin`, `is_superuser`, `is_active`.
    - Allows searching by `email` and `username`.
    - Orders the list view by `email`.
    - Overrides `get_model_perms` to customize permissions for displaying the model in the admin interface:
        - If the user is a superuser and a tenant admin, grants full permissions.
        - Otherwise, defaults to the parent class’s behavior.

2. `DomainAdmin`:
    - Custom admin interface for the `Domain` model.
    - Overrides `get_model_perms` to customize permissions for displaying the model in the admin interface:
        - If the user is a superuser and a tenant admin, grants full permissions.
        - Otherwise, defaults to the parent class’s behavior.

3. `TenantAdmin`:
    - Custom admin interface for the `Tenant` model.
    - Overrides `get_model_perms` to customize permissions for displaying the model in the admin interface:
        - If the user is a superuser and a tenant admin, grants full permissions.
        - Otherwise, defaults to the parent class’s behavior.

Model Registration:
- Unregisters existing admin interfaces for the `CustomUser`, `Domain`, and `Tenant` models if they are already registered.
- Registers the `CustomUser`, `Domain`, and `Tenant` models with their respective custom admin classes (`CustomUserAdmin`, `DomainAdmin`, and `TenantAdmin`).

Dependencies:
- `admin` and `UserAdmin` from `django.contrib` for customizing the Django admin interface.
- `CustomUser`, `Domain`, and `Tenant` models from the application's models.

This setup ensures that the admin interface for the application is customized to fit the multi-tenant architecture, with specific permission handling for different user roles.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Domain, Tenant


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("email", "username", "is_tenant_admin", "is_superuser", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)

    def get_model_perms(self, request):
        user = request.user
        if user.is_superuser and user.is_tenant_admin:
            return {}
        return super().get_model_perms(request)


# Custom admin class for Domain
class DomainAdmin(admin.ModelAdmin):
    model = Domain

    def get_model_perms(self, request):
        user = request.user
        if user.is_superuser and user.is_tenant_admin:
            return {}
        return super().get_model_perms(request)


# Custom admin class for Tenant
class TenantAdmin(admin.ModelAdmin):
    model = Tenant

    def get_model_perms(self, request):
        user = request.user
        if user.is_superuser and user.is_tenant_admin:
            return {}
        return super().get_model_perms(request)


# Check if the CustomUser model is registered before unregistering
if admin.site.is_registered(CustomUser):
    admin.site.unregister(CustomUser)

admin.site.register(CustomUser, CustomUserAdmin)

# Check if the Domain model is registered before unregistering
if admin.site.is_registered(Domain):
    admin.site.unregister(Domain)

admin.site.register(Domain, DomainAdmin)

# Check if the Tenant model is registered before unregistering
if admin.site.is_registered(Tenant):
    admin.site.unregister(Tenant)

admin.site.register(Tenant, TenantAdmin)
