"""
This module defines models and a custom user manager for a multi-tenant application.

Models:
1. `Tenant`:
    - Inherits from `TenantMixin` to support multi-tenancy.
    - Fields:
        - `name`: CharField with a maximum length of 100 characters. Represents the name of the tenant.
        - `address`: Optional CharField with a maximum length of 255 characters. Represents the address of the tenant.
        - `registration_number`: Optional CharField with a maximum length of 255 characters. Represents the registration number of the tenant.
        - `created_at`: DateField that auto-fills with the current date when the tenant is created. Represents the creation date of the tenant.
        - `auto_create_schema`: Boolean field that is set to True, indicating that the schema for new tenants should be automatically created.

2. `Domain`:
    - Inherits from `DomainMixin` to support multi-tenancy.
    - This model is intended to represent a domain associated with a tenant. The model currently does not have additional fields beyond those provided by `DomainMixin`.

3. `CustomUserManager`:
    - Custom manager for the `CustomUser` model.
    - Methods:
        - `create_user(email, tenant, password=None, **extra_fields)`:
            - Creates and returns a regular user with the specified email, tenant, and password.
            - Normalizes the email address and sets the user's password before saving.
        - `create_superuser(email, password=None, tenant=None, **extra_fields)`:
            - Creates and returns a superuser with the specified email, password, and tenant.
            - Ensures that `is_superuser` and `is_staff` fields are set to True.

4. `CustomUser`:
    - Inherits from `AbstractBaseUser` and `PermissionsMixin` to provide custom user functionality and permissions.
    - Fields:
        - `email`: EmailField. Represents the user's email address and is used as the unique identifier.
        - `username`: Optional CharField with a maximum length of 255 characters. Represents the user's username.
        - `is_tenant_admin`: BooleanField indicating whether the user is a tenant administrator.
        - `is_staff`: BooleanField indicating whether the user has staff status.
        - `is_active`: BooleanField indicating whether the user account is active.
        - `date_joined`: DateTimeField with a default value of the current time. Represents the date and time the user joined.
        - `tenant`: ForeignKey to the `Tenant` model. Represents the tenant to which the user belongs.
    - Manager:
        - `objects`: An instance of `CustomUserManager` for user creation and management.
    - Meta:
        - `unique_together`: Enforces uniqueness for the combination of email and tenant.
    - Methods:
        - `__str__()`: Returns a string representation of the user, including the email and tenant.

Dependencies:
- `AbstractBaseUser`, `PermissionsMixin`, and `BaseUserManager` from `django.contrib.auth.models` for user management and authentication.
- `models` from `django.db` for defining database models and fields.
- `timezone` from `django.utils` for handling time-related fields.
- `TenantMixin` and `DomainMixin` from `django_tenants.models` to support multi-tenancy.

This file provides the core models and user management functionality for a multi-tenant application, including tenant management, user creation, and permissions handling.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    auto_create_schema = True  # Automatically create schema for new tenants


class Domain(DomainMixin):
    # Domain associated with the tenant
    pass


class CustomUserManager(BaseUserManager):
    def create_user(self, email, tenant, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tenant=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email=email, password=password, tenant=tenant, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField()
    username = models.CharField(max_length=255, blank=True, null=True)
    is_tenant_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        unique_together = (
            "email",
            "tenant",
        )  # Enforce uniqueness on the combination of email and tenant

    def __str__(self):
        return f"{self.email} ({self.tenant})"
