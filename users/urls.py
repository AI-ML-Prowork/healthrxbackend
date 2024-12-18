"""
This module defines the URL routing for the application, including API endpoints and schema documentation.

URL Patterns:
1. `admin/`:
    - Routed to Django's built-in admin site.
    - Provides the administrative interface for managing application data.

2. `create-tenant`:
    - Routed to the `TenantRegister` view.
    - Endpoint for registering new tenants.
    - Uses the `POST` method to create a new tenant.

3. `check-tenant`:
    - Routed to the `CheckTenant` view.
    - Endpoint for checking the existence of a tenant.
    - Uses the `GET` method to verify if a tenant with a specified username exists.

4. `swagger(?P<format>\.json|\.yaml)`:
    - Routed to the DRF schema view for API documentation in JSON or YAML format.
    - Provides the OpenAPI schema without UI for integration with external tools.

5. `docs/`:
    - Routed to the DRF schema view with Swagger UI.
    - Provides interactive API documentation with Swagger UI.

6. `redoc/`:
    - Routed to the DRF schema view with ReDoc UI.
    - Provides interactive API documentation with ReDoc UI.

Schema View:
- `schema_view`:
    - Configured using `drf_yasg` to generate and serve API documentation.
    - Displays API documentation with options for Swagger and ReDoc interfaces.
    - Publicly accessible with `permissions.AllowAny`, meaning no authentication is required to view the documentation.

Dependencies:
- `admin` from `django.contrib` for the admin interface.
- `TenantRegister` and `CheckTenant` views from the application's views.
- `permissions` from `rest_framework` for setting API permissions.
- `get_schema_view` and `openapi` from `drf_yasg` for generating API documentation.
- `path` and `re_path` from `django.urls` for routing URL patterns.

This file sets up the routing for the Django application, including endpoints for tenant management and comprehensive API documentation.
"""
"""
This module defines the URL routing for the application, including API endpoints and schema documentation.

URL Patterns:
1. admin/:
    - Routed to Django's built-in admin site.
    - Provides the administrative interface for managing application data.

2. create-tenant:
    - Routed to the TenantRegister view.
    - Endpoint for registering new tenants.
    - Uses the POST method to create a new tenant.

3. check-tenant:
    - Routed to the CheckTenant view.
    - Endpoint for checking the existence of a tenant.
    - Uses the GET method to verify if a tenant with a specified username exists.

4. swagger(?P<format>\.json|\.yaml):
    - Routed to the DRF schema view for API documentation in JSON or YAML format.
    - Provides the OpenAPI schema without UI for integration with external tools.

5. docs/:
    - Routed to the DRF schema view with Swagger UI.
    - Provides interactive API documentation with Swagger UI.

6. redoc/:
    - Routed to the DRF schema view with ReDoc UI.
    - Provides interactive API documentation with ReDoc UI.

Schema View:
- schema_view:
    - Configured using drf_yasg to generate and serve API documentation.
    - Displays API documentation with options for Swagger and ReDoc interfaces.
    - Publicly accessible with permissions.AllowAny, meaning no authentication is required to view the documentation.

Dependencies:
- admin from django.contrib for the admin interface.
- TenantRegister and CheckTenant views from the application's views.
- permissions from rest_framework for setting API permissions.
- get_schema_view and openapi from drf_yasg for generating API documentation.
- path and re_path from django.urls for routing URL patterns.

This file sets up the routing for the Django application, including endpoints for tenant management and comprehensive API documentation.
"""

from django.contrib import admin
from .views import CheckTenant, TenantRegister
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from clients.views import TenantView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(title="Tenant API",default_version="v1",description="API documentation for Multi-tenant Project",),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # for the super admin(saas login)
    path("admin", admin.site.urls),
    path('api/superadmin-login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', CustomUserListView.as_view(), name='custom-user-list'),
    path('domains', DomainListView.as_view(), name='domain-list'),
    path('tenants', TenantListView.as_view(), name='tenant-list'),



    path("tenant", TenantRegister.as_view(), name="tenant-register"),
    path("check-tenant", CheckTenant.as_view(), name="check-tenant"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$",schema_view.without_ui(cache_timeout=0),name="schema-json"),
    path("docs/",schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]