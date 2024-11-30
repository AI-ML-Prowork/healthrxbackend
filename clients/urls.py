"""
This module defines the URL routing for the application, including API endpoints for user and blog operations.

URL Patterns:
1. `admin/`:
    - Routed to Django's built-in admin site.
    - Provides the administrative interface for managing application data.

2. `''` (empty path):
    - Routed to the `index` view.
    - Provides a basic view that returns a JSON response with the current tenant's context.

3. `user/register`:
    - Routed to the `UserRegister` view.
    - Endpoint for user registration.
    - Uses the `POST` method to create a new user.

4. `login`:
    - Routed to the `UserLoginView` view.
    - Endpoint for user authentication.
    - Uses the `POST` method to log in users and return authentication tokens.

5. `blog`:
    - Routed to the `BlogView` view.
    - Endpoint for managing blog posts.
    - Supports `POST`, `GET`, `PATCH`, and `DELETE` methods for creating, retrieving, updating, and deleting blog posts.

6. `tenant/user`:
    - Routed to the `TenantView` view.
    - Endpoint for tenant-specific user management.
    - Supports `GET`, `PATCH`, and `DELETE` methods for retrieving, updating, and deleting user profiles by tenant admins.

7. `search/` (commented out):
    - Routed to the `BlogSearchView` view (commented out for potential future use).
    - Intended for searching blog posts based on a query parameter.
    - Supports the `GET` method and utilizes Elasticsearch for search functionality.

Dependencies:
- `admin` from `django.contrib` for the admin interface.
- `path` and `include` from `django.urls` for URL routing.
- Various views (`index`, `UserRegister`, `UserLoginView`, `BlogView`, `TenantView`) from the application's views module.

This file sets up the routing configuration for the application, providing endpoints for core functionalities including user registration, login, blog management, and tenant-specific user operations.
"""

from django.contrib import admin
from django.urls import path
from .views import index
from .views import (
    UserRegister,
    UserLoginView,
    BlogView,
    TenantView,
    BlogManagementView,
    TenantManagementView,
    UserView,
    FetchAllBlogs,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),

    # for the user system..
    path("user/register", UserRegister.as_view(), name="user-register"),
    path("login", UserLoginView.as_view(), name="user-login"),
    path("tenant/user", TenantView.as_view(), name="tenant-view"),
    path("tenant/user/<int:user_id>",TenantManagementView.as_view(),name="tenant-manage"),
    path("user/detail", UserView.as_view(), name="user-detail"),

    # for blog system..
    path("blog", BlogView.as_view(), name="blog"),
    path("blog/<int:blog_id>", BlogManagementView.as_view(), name="blog-manage"),
    path("all-blogs", FetchAllBlogs.as_view(), name="Get-all-blogs"),

]
