"""
This module defines API views for handling user and blog operations in a multi-tenant environment.

Views:
1. `index(request)`:
    - Endpoint for a basic view that returns a JSON response with a message indicating the current tenant's context.

2. `UserRegister(APIView)`:
    - Handles user registration.
    - Method: `POST`
    - Receives user registration data, validates it using `UserRegisterSerializer`, and creates a new user if valid.
    - Returns a success message or error details based on the result of the operation.

3. `UserLoginView(APIView)`:
    - Handles user authentication.
    - Method: `POST`
    - Receives email and password, and uses `TenantEmailBackend` for authentication.
    - Returns an authentication token if successful, or an error message if authentication fails.
    - Differentiates between tenant users and tenant admins.

4. BlogView(APIView)`:
    - Manages blog-related operations.
    - Method: `POST`:
        - Creates a new blog post associated with the current user and tenant.
        - Also adds blog to specific elastic search index
    - Method: `GET`:
        - Retrieves blog posts. Allows filtering by `blog_id` and user.
    - Method: `PATCH`:
        - Updates a blog post. Allows partial updates and ensures the operation is scoped to the current user or tenant admin.
    - Method: `DELETE`:
        - Deletes a blog post identified by `blog_id`. Ensures the deletion is scoped to the current user or tenant admin.

5. `TenantView(APIView)`:
    - Manages tenant-specific user operations.
    - Method: `GET`:
        - Retrieves user profiles for tenant admins. Allows filtering by `user_id`.
    - Method: `PATCH`:
        - Updates user profiles. Allows partial updates and is restricted to tenant admins.
    - Method: `DELETE`:
        - Deletes a user profile identified by `user_id`. Ensures the operation is performed by a tenant admin.

6. `FetchAllBlogs(APIView)`:
    - Method: `GET`:
    - Simply fetches all blogs as per the tenant.


Dependencies:
- `logging` for logging messages and errors.
- `JsonResponse` from `django.http` for standard JSON responses.
- `APIView`, `Response`, `status`, and `filters` from `rest_framework` for API views and responses.
- `TenantEmailBackend` for custom authentication backend.
- `get_tokens_for_user` for generating authentication tokens.
- `IsTenantAdmin` from `custom_permissions` for custom permission handling.
- `swagger_auto_schema` and `openapi` from `drf_yasg` for API documentation.
- `IsAuthenticated` for securing views.
- `UserRegisterSerializer`, `UserLoginSerializer`, `BlogSerializer`, `UserSerializer` from `serializers` for data validation and serialization.
- `UserProfile`, `Blog` models for user and blog data management.

This file sets up the API endpoints for user and blog management in a multi-tenant system and includes a commented-out search view for potential future use.
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    BlogSerializer,
    UserSerializer,
)
from .models import UserProfile, CustomUser, Blog

from users.auth_backends import TenantEmailBackend
from .helpers import get_tokens_for_user
from .custom_permissions import IsTenantAdmin, IsTenantAdminOrIsUserPartOfTenant
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from search.documents import BlogDocument
from .models import Tenant


logger = logging.getLogger(__name__)


def index(request):
    context = f"you are at {request.tenant} view"
    return JsonResponse({"msg": context})


def add_blog_to_index(request, blog):
    """View to add a blog to the tenant-specific index."""
    tenant_name = request.tenant.name
    # Get the tenant-specific document
    blog_document = BlogDocument.for_tenant(tenant_name)

    # Add the blog to Elasticsearch
    blog_document.update(blog)

    logger.info(f"New tanant '{tenant_name}' added to elastic search index.")
    return JsonResponse(
        {"status": "indexed", "tenant": tenant_name, "blog_title": blog.title}
    )


class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            logger.info("user created!")
            return Response(
                {"data": serializer.data, "msg": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )

        logger.error(f"something went wrong {serializer.errors}")
        return Response(
            {"data": serializer.errors, "msg": "Something went wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        is_user = TenantEmailBackend().authenticate(
            request, email=email, password=password, tenant=request.tenant
        )
        if is_user is not None:
            try:
                _ = UserProfile.objects.get(user=is_user)
                token = get_tokens_for_user(is_user)
                logger.info("tenant user logged in!")
                return Response(
                    {
                        "email": str(is_user),
                        "username": is_user.username,
                        "msg": "User Logged in Successfully!",
                        "is_tenant_admin": is_user.is_tenant_admin,
                        "access_token": token,
                    },
                    status=status.HTTP_200_OK,
                )

            except UserProfile.DoesNotExist:
                logger.info("Checking if tenant admin is trying to login!")
                try:
                    _ = CustomUser.objects.get(email=is_user.email)
                    if is_user.is_tenant_admin:
                        logger.info("tenant admin logged in!")
                        token = get_tokens_for_user(is_user)
                        return Response(
                            {
                                "email": str(is_user),
                                "username": is_user.username,
                                "msg": "Tenant admin Logged in Successfully!",
                                "is_tenant_admin": is_user.is_tenant_admin,
                                "access_token": token,
                            },
                            status=status.HTTP_200_OK,
                        )
                except CustomUser.DoesNotExist as e:
                    logger.critical(f"User login went wrong {e}")
                    return Response(
                        {"msg": f"user {is_user} does not exist in this tenant!"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            return Response(
                {"msg": f"User {is_user} doesn't exist in this tenant!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        logger.critical("Authentication failed!")
        return Response(
            {
                "data": serializer.errors,
                "msg": "Unfortunately the credentials you are entering is not matching our records."
                "Please try again later or try resetting the credentials",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class BlogView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    @swagger_auto_schema(
        request_body=BlogSerializer,
        responses={200: "Success", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(user=request.user, tenant=request.tenant)
            logger.info("Blog added!")

            add_blog_to_index(request, blog)

            return Response(
                {"msg": "Blog added Successfully!", "blog_id": blog.id},
                status=status.HTTP_200_OK,
            )

        logger.error(f"something went wrong while adding blog {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):

        logger.info("getting blogs with respect to tenant and user!")
        blogs = Blog.objects.filter(user=request.user)

        serializer = BlogSerializer(blogs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class FetchAllBlogs(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]
    def get(self, request):

        logger.info("getting all blogs respect to their own tenant!")
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



class BlogManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "blog_id",
                openapi.IN_QUERY,
                description="Blog id",
                type=openapi.TYPE_INTEGER,
            )
        ],
        request_body=BlogSerializer,
        responses={200: "Success", 400: "Bad Request"},
    )
    def get(self, request, blog_id):
        try:
            if request.user.is_tenant_admin:
                logger.info(
                    "getting blog for admin with respect to their own tenant and blog_id!"
                )
                blog_instance = Blog.objects.get(id=blog_id)
            else:
                logger.info("getting blog with respect to tenant, blog id and user!")
                blog_instance = Blog.objects.get(id=blog_id, user=request.user)

        except Blog.DoesNotExist as e:
            logger.critical(f"Getting blog went wrong: {e}")
            return Response(
                {"msg": f"Blog with this {blog_id} not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BlogSerializer(blog_instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, blog_id):
        try:
            if request.user.is_tenant_admin:
                logger.info("Getting blog for admin to patch with respect to blog_id!")
                blog_instance = Blog.objects.get(id=blog_id)
            else:
                logger.info("Getting blog to patch with respect to blog_id and user!")
                blog_instance = Blog.objects.get(id=blog_id, user=request.user)
        except Blog.DoesNotExist as e:
            logger.critical(f"Getting blog during patch went wrong: {e}")
            return Response(
                {"msg": f"Blog with this {blog_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BlogSerializer(blog_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response(
                {"msg": "Blog Updated Successfully!"}, status=status.HTTP_200_OK
            )

        logger.error(f"Getting blog during patch went wrong {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, blog_id):
        try:
            if request.user.is_tenant_admin:
                logger.info("Getting blog for admin to delete with respect to blog_id!")
                blog_instance = Blog.objects.get(id=blog_id)
            else:
                logger.info("Getting blog to delete with respect to blog_id and user!")
                blog_instance = Blog.objects.get(id=blog_id, user=request.user)

        except Blog.DoesNotExist as e:
            logger.critical(f"while deleting blog something went wrong {e}")
            return Response(
                {"msg": f"Blog with this {blog_id} not found or already deleted!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        blog_instance.delete()
        logger.info("Blog Deleted!")
        return Response(
            {"msg": "Blog Deleted Successfully!"}, status=status.HTTP_200_OK
        )


class TenantView(APIView):
    permission_classes = [IsTenantAdmin]

    def get(self, request):
        logger.info("Getting all user for tenant admin!")
        users = UserProfile.objects.all()
        users = Tenant.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_obj = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(
                {"msg": f" {request.user} doesn't exists!"}, status=status.HTTP_200_OK
            )

        serializer = UserSerializer(user_obj)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class TenantManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, user_id):
        try:
            logger.info("Getting user for tenant admin with user_id!")
            user_instance = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist as e:
            logger.critical(
                f"Something went wrong while getting user with {user_id}: {e}"
            )
            return Response(
                {"msg": f"User with this {user_id} not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user_instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            if request.user.is_tenant_admin:
                logger.info("Getting user for tenant admin with user_id for patch!")
                user_instance = UserProfile.objects.get(id=user_id)
            else:
                logger.info("Getting user with user_id for patch!")
                user_instance = UserProfile.objects.get(user=request.user)

        except UserProfile.DoesNotExist as e:
            logger.critical(
                f"Something went wrong while getting user for patch with {user_id}: {e}"
            )
            return Response(
                {"msg": f"User with this {user_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "User Updated Successfully!"}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, user_id):
        try:
            if request.user.is_tenant_admin:
                logger.info("Getting user for tenant admin with user_id for delete!")
                user_instance = UserProfile.objects.get(id=user_id)
            else:
                logger.info("Getting user with user_id for delete!")
                user_instance = UserProfile.objects.get(user=request.user)

        except UserProfile.DoesNotExist as e:
            logger.critical(
                f"Something went wrong while getting user for delete with {user_id}: {e}"
            )
            return Response(
                {"msg": f"User with this {user_id} not found or already deleted"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_instance.delete()
        return Response(
            {"msg": "User Deleted Successfully!"}, status=status.HTTP_200_OK
        )
