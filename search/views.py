"""
BlogSearchView(APIView)`:
    - Provides search functionality for blog posts.
    - Method: `GET`
    - Accepts a query parameter for searching blog posts based on title and description.
    - Uses Elasticsearch for performing the search
    - Searches by dynamic index
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant

from rest_framework.permissions import IsAuthenticated
from elasticsearch_dsl.query import MultiMatch
from search.documents import BlogDocument

logger = logging.getLogger(__name__)


class BlogSearchView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request):
        """View to search for blogs in the tenant-specific index."""
        query = request.GET.get("q", "")
        tenant_name = request.tenant.name

        # Get the tenant-specific document
        blog_document = BlogDocument.for_tenant(tenant_name)

        # Perform the search on the tenant-specific index
        search_query = MultiMatch(query=query, fields=["title", "description"])
        blogs = blog_document.search().query(search_query).execute()
        data = {"data": [blog.to_dict() for blog in blogs]}

        logger.info(f"ELSearch: Blogs fetched from {tenant_name} schema: {data}")
        return Response(
            {"data": [blog.to_dict() for blog in blogs]}, status=status.HTTP_200_OK
        )
