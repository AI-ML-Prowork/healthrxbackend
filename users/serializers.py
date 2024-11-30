"""
This module defines serializers for tenant registration in the application.

Serializers:
1. `TenantRegisterSerializer`:
    - A serializer class for handling the registration of new tenants.
    - Fields:
        - `username`: Required `CharField` with a maximum length of 100 characters. Represents the schema name for the tenant.
        - `address`: Optional `CharField` with a maximum length of 255 characters. Represents the address of the tenant.
        - `registration_number`: Optional `CharField` with a maximum length of 255 characters. Represents the registration number of the tenant.
        - `company_name`: Required `CharField` with a maximum length of 100 characters. Represents the company name of the tenant.
        - `email`: Required `EmailField`. Represents the email address of the tenant admin.
        - `first_name`: Required `CharField` with a maximum length of 255 characters. Represents the first name of the tenant admin.
        - `password`: Required `CharField`. Write-only field for the password of the tenant admin.

    Methods:
    - `validate_username(value)`:
        - Ensures that the provided `username` (tenant schema name) is unique.
        - Raises `ValidationError` if a tenant with the same schema name already exists.

    - `create(validated_data)`:
        - Creates a new `Tenant` instance with the provided validated data.
        - Creates a primary `Domain` instance associated with the newly created tenant.
        - Creates a new `CustomUser` instance for the tenant admin with the provided email, username (as first name), and password.
        - Returns a dictionary containing the newly created tenant, domain, username, and user details.

Dependencies:
- `serializers` from Django REST Framework for serializing and validating data.
- `Tenant`, `Domain`, and `CustomUser` models for creating and managing tenant-related data.

This serializer handles the complete registration process for new tenants, including tenant, domain, and user creation, and ensures data integrity and uniqueness.
"""

from rest_framework import serializers
from .models import Tenant, Domain, CustomUser


class TenantRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    registration_number = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    company_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if Tenant.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Tenant name already taken.")
        return value

    def create(self, validated_data):
        # Tenant creation
        tenant = Tenant.objects.create(
            schema_name=validated_data["username"],
            address=validated_data.get("address"),
            registration_number=validated_data.get("registration_number"),
            name=validated_data["company_name"],
        )

        # Domain creation
        full_domain = self.context["request"].get_host()
        domain_parts = full_domain.split(":")
        domain = f'{validated_data["username"]}.{domain_parts[0]}'
        Domain.objects.create(domain=domain, tenant=tenant, is_primary=True)

        # User creation
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["first_name"],
            password=validated_data["password"],
            tenant=tenant,
            is_tenant_admin=True,
            is_superuser=True,
            is_staff=True,
        )

        return {
            "tenant": tenant,
            "domain": full_domain,
            "username": validated_data["username"],
            "user": user,
        }
