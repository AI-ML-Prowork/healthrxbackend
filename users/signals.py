"""
This module contains signal handlers for Django's post-migrate signal.

Signal Handlers:
1. `create_default_tenant`:
    - Connected to the `post_migrate` signal, which is emitted after migrations have been applied.
    - Checks if a default tenant with the schema name "public" exists.
    - If the default tenant does not exist, creates it with the name "Public".
    - Also creates a primary domain entry associated with this tenant, with the domain set to the production host.

Dependencies:
- `post_migrate` signal from `django.db.models.signals` to execute logic after database migrations.
- `receiver` decorator from `django.dispatch` to connect the signal with the handler function.
- `Tenant` and `Domain` models to interact with the database and create the default tenant and domain.

This setup ensures that a default tenant and domain are available after migrations, which is useful for setting up initial configurations or default data required for the application.
"""

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tenant, Domain

# from search.documents import BlogDocument

PRODUCTION_DOMAIN = "healthrxbackend.onrender.com"

@receiver(post_migrate)
def create_default_tenant(sender, **kwargs):
    if not Tenant.objects.filter(schema_name="public").exists():
        # BlogDocument.init()
        tenant = Tenant.objects.create(schema_name="public", name="Public")
        tenant.save()

        domain = Domain.objects.create(
            domain=PRODUCTION_DOMAIN, tenant=tenant, is_primary=True
        )
        domain.save()
