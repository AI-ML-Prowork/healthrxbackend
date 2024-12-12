"""
This module contains views related to tenant management in the application.

It includes:
- A public view function to check the availability of the service.
- An API view to handle the registration of new tenants.
- An API view to check if a tenant exists in the system.

Views:
1. `index`:
    - Handles HTTP GET requests.
    - Provides a public endpoint to confirm that the service is reachable.
    - Returns a JSON response with a message indicating that the user is at the public view.

2. `TenantRegister`:
    - Handles HTTP POST requests to register a new tenant.
    - Uses `TenantRegisterSerializer` to validate and save tenant data.
    - Logs the registration attempt and errors if validation fails.
    - On successful registration, returns a JSON response containing a success message, tenant URL, and user data.
    - On failure, returns a JSON response with validation errors.
    - Also, creates a new index on elastic search server for isolated quick searching.

3. `CheckTenant`:
    - Handles HTTP GET requests to verify if a tenant exists.
    - Retrieves the `username` from query parameters to check the presence of a tenant with that schema name.
    - Logs the check attempt and returns a JSON response indicating whether the tenant exists or not.

Logging:
- Logs are configured to track the flow of tenant registration and existence checks, including errors.

Dependencies:
- Django's `JsonResponse` for public view responses.
- Django REST Framework's `APIView`, `Response`, and `status` for API views.
- `TenantRegisterSerializer` for serializing and validating tenant data.
- `Tenant` model to query and check tenant existence.
- Python's `logging` module for logging information and errors.
"""

from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Tenant
import logging
from rest_framework.permissions import IsAdminUser
from search.documents import BlogDocument


# for the super admin (saas login)
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, Domain, Tenant
from .serializers import CustomUserSerializer, DomainSerializer, TenantSerializer, TenantRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .permissions import IsGlobalSuperAdmin


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Ensure the user is a global superuser
        if not user.is_superuser or user.tenant is not None:
            raise AuthenticationFailed("Only global superusers are allowed to generate tokens.")

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class TenantListView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsGlobalSuperAdmin]


class DomainListView(generics.ListCreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsGlobalSuperAdmin]


class CustomUserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsGlobalSuperAdmin]
# for the super admin (saas login) end







def create_index_for_tenant(tenant_name):
    """Create an Elasticsearch index for a new tenant."""
    blog_document = BlogDocument.for_tenant(tenant_name)

    # Create the index
    blog_document._index.create(ignore=400)

    logger.info(f"Index {blog_document._index._name} created for tenant {tenant_name}")


logger = logging.getLogger(__name__)


def index(request):
    context = "you are at public view"
    return JsonResponse({"msg": context})


class TenantRegister(APIView):
    def post(self, request):
        logger.info("Registering New tenant!")
        serializer = TenantRegisterSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            data = serializer.save()
            response_data = {
                "msg": "Tenant created successfully!",
                "tenant_url": f'http://{data["username"]}.{data["domain"]}',
                "user_data": {
                    "email": data["user"].email,
                    "username": data["user"].username,
                },
            }
            create_index_for_tenant(data["username"])
            return Response(response_data, status=status.HTTP_201_CREATED)
        logger.error("Something went wrong!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckTenant(APIView):
    def get(self, request):
        username = request.query_params.get("username", None)
        logger.info("Checking if the tenant exists!")
        if Tenant.objects.filter(schema_name=username).exists():
            return Response({"msg": True}, status=status.HTTP_200_OK)

        return Response({"msg": False}, status=status.HTTP_404_NOT_FOUND)
