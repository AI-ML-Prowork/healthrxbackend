# # """
# # This module defines a custom authentication backend for tenant-based authentication.
# #
# # Authentication Backend:
# # 1. `TenantEmailBackend`:
# #     - Inherits from `ModelBackend` to provide custom authentication logic for users.
# #     - Methods:
# #         - `authenticate(request, email=None, password=None, tenant=None, **kwargs)`:
# #             - Authenticates a user based on their email, password, and tenant.
# #             - Parameters:
# #                 - `request`: The HTTP request object.
# #                 - `email`: The email address of the user attempting to authenticate.
# #                 - `password`: The password provided by the user.
# #                 - `tenant`: The tenant to which the user belongs.
# #                 - `**kwargs`: Additional keyword arguments.
# #             - Process:
# #                 - Retrieves the `CustomUser` instance matching the provided email and tenant.
# #                 - Checks if the user exists and if the provided password is correct.
# #                 - Verifies that the user can be authenticated.
# #                 - Returns the user instance if authentication is successful; otherwise, returns `None`.
# #
# # Dependencies:
# # - `ModelBackend` from `django.contrib.auth.backends` to extend the default authentication backend.
# # - `CustomUser` model from the application's models to perform user authentication.
# #
# # This backend allows for authentication of users based on both their email and tenant, ensuring that the authentication process respects multi-tenancy constraints.
# # """
# #
# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser
#
#
# class TenantEmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, tenant=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(email=email, tenant=tenant)
#             if self.check_password(user, password):
#                 return user
#         except CustomUser.DoesNotExist:
#             try:
#                 user = CustomUser.objects.get(email=email)
#                 if self.check_password(user, password):
#                     return user
#             except  CustomUser.DoesNotExist:
#                 return None
#         return None
#     def check_password(self, user, password):
#         return user.check_password(password) and self.user_can_authenticate(user)
#


"""
This module defines a custom authentication backend for tenant-based authentication.

Authentication Backend:
1. `TenantEmailBackend`:
    - Inherits from `ModelBackend` to provide custom authentication logic for users.
    - Methods:
        - `authenticate(request, email=None, password=None, tenant=None, **kwargs)`:
            - Authenticates a user based on their email, password, and tenant.
            - Parameters:
                - `request`: The HTTP request object.
                - `email`: The email address of the user attempting to authenticate.
                - `password`: The password provided by the user.
                - `tenant`: The tenant to which the user belongs.
                - `**kwargs`: Additional keyword arguments.
            - Process:
                - Retrieves the `CustomUser` instance matching the provided email and tenant.
                - Checks if the user exists and if the provided password is correct.
                - Verifies that the user can be authenticated.
                - Returns the user instance if authentication is successful; otherwise, returns `None`.

Dependencies:
- `ModelBackend` from `django.contrib.auth.backends` to extend the default authentication backend.
- `CustomUser` model from the application's models to perform user authentication.

This backend allows for authentication of users based on both their email and tenant, ensuring that the authentication process respects multi-tenancy constraints.
"""

from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class TenantEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, tenant=None, **kwargs):
        post_data = request.__dict__.get('_post', {})
        if not email:
            email = post_data.get('username')
        if not password:
            password = post_data.get('password')
        if request.tenant.name != "Public":
            tenant = request.tenant
        try:
            user = CustomUser.objects.get(email=email, tenant=tenant)

        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
