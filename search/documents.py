"""
Elasticsearch Document class for indexing and searching blog posts for a multi-tenant application.

This class defines the fields and model for indexing blog posts in Elasticsearch using Django Elasticsearch DSL. It also allows dynamic creation of separate indices for each tenant.

Classes:
    BlogDocument: Defines the Elasticsearch document structure for the `Blog` model.

Attributes:
    Django.model (Blog): The model to be indexed in Elasticsearch.
    Django.fields (list): List of fields to be indexed from the `Blog` model.
    Index.name (str): Base name for the Elasticsearch index, which will be dynamically modified for each tenant.

Methods:
    for_tenant(tenant_name):
        Returns an instance of BlogDocument with the index name dynamically set based on the tenant name.
        This allows for the creation of tenant-specific indices in Elasticsearch.
"""

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from clients.models import Blog


@registry.register_document
class BlogDocument(Document):
    class Django:
        model = Blog
        fields = [
            "title",
            "description",
            "created_at",
        ]

    class Index:
        # Create a separate index for each tenant using the tenant name
        name = "blogs"

    @classmethod
    def for_tenant(cls, tenant_name):
        """Return an instance of BlogDocument with a dynamic index."""
        instance = cls()
        instance._index._name = f"{tenant_name}_blogs"
        return instance
