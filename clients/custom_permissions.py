"""
This module defines custom permissions for controlling access to views based on tenant admin status.

Classes:
- `IsTenantAdmin`:
    - A custom permission class that grants access only to users who are tenant admins.
    - Inherits from `BasePermission` provided by Django REST Framework.

    Methods:
    - `has_permission(self, request, view)`:
        - Checks if the request should be granted access based on tenant admin status.
        - Returns `True` if the user is authenticated and has the `is_tenant_admin` attribute set to `True`.
        - Returns `False` otherwise.

    Usage:
    - This permission class is used in views to restrict access so that only users who are designated as tenant admins can access the view.
    - It is typically applied in the `permission_classes` attribute of a view or viewset.

Dependencies:
- `BasePermission` from `rest_framework.permissions` for creating custom permissions.

This file provides a custom permission class that ensures only tenant admins can access specific views in the application.
"""

from rest_framework.permissions import BasePermission
from clients.models import UserProfile
from users.models import CustomUser


class IsTenantAdmin(BasePermission):
    """
    Custom permission to check if the user is admin of the tenant.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_tenant_admin
            and CustomUser.objects.filter(
                username=request.user.username, tenant=request.tenant
            ).exists()
        )


class IsUserPartOfTenant(BasePermission):
    """
    Custom permission to check if the user is part of the tenant.
    """

    def has_permission(self, request, view):

        return UserProfile.objects.filter(
            user=request.user, tenant=request.tenant
        ).exists()


class IsTenantAdminOrIsUserPartOfTenant(BasePermission):
    """
    Custom permission to check if the user is admin and a part of the tenant.
    """

    def has_permission(self, request, view):
        if IsTenantAdmin().has_permission(request, view):
            return True

        return UserProfile.objects.filter(
            user=request.user, tenant=request.tenant
        ).exists()
