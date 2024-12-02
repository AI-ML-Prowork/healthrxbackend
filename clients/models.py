"""
This module defines the database models for user profiles and blog posts used in the application.

Models:
1. `UserProfile`:
    - Represents additional profile information for users.
    - Fields:
        - `user`: A foreign key linking to the `CustomUser` model. Represents the user to whom this profile belongs.
        - `tenant`: A foreign key linking to the `Tenant` model. Represents the tenant associated with this profile. This field is nullable.
        - `phone`: An integer field to store the user's phone number. This field is optional (blank=True, null=True).

    - Usage: Used to store additional details about users such as their phone number and associated tenant.

2. `Blog`:
    - Represents a blog post created by users.
    - Fields:
        - `user`: A foreign key linking to the `CustomUser` model. Represents the user who created the blog post.
        - `tenant`: A foreign key linking to the `Tenant` model. Represents the tenant associated with the blog post. This field is nullable.
        - `title`: A character field to store the title of the blog post. It is optional (blank=True, null=True).
        - `description`: A text field to store the content or description of the blog post. It is optional (blank=True, null=True).
        - `created_at`: A date field that automatically records the date when the blog post was created. This field is optional (auto_now_add=True, null=True, blank=True).

    - Methods:
        - `__str__(self)`: Returns a string representation of the blog post in the format "title-user".

    - Usage: Used to store and manage blog posts within the application, including details like title, content, creation date, and associated user and tenant.

Dependencies:
- `models` from `django.db` for defining the database models.
- `CustomUser`, `Tenant` from the `users.models` module for foreign key relationships.

This file provides the models for handling user profiles and blog posts, including their fields and relationships with other models in the application.
"""

from django.db import models
from users.models import CustomUser, Tenant
from django_tenants.models import TenantMixin


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)
    phone = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user


class Blog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title}-{self.user}"


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    auto_create_schema = True  # Automatically create schema for new tenants