"""
This module provides functionality for generating JSON Web Tokens (JWT) for user authorization.

Function:
- `get_tokens_for_user(user)`:
    - Generates JWT tokens for the given user.
    - Uses the `RefreshToken` class from `rest_framework_simplejwt.tokens` to create a refresh token and an access token.
    - Returns a dictionary containing:
        - `refresh`: The refresh token as a string.
        - `access`: The access token as a string.

    Parameters:
    - `user`: An instance of the `CustomUser` model for which the tokens are generated.

    Returns:
    - A dictionary with two keys:
        - `'refresh'`: The refresh token as a string.
        - `'access'`: The access token as a string.

    Usage:
    - This function is typically used to generate JWT tokens upon user authentication, allowing the user to access protected resources and refresh their authentication session.

Dependencies:
- `RefreshToken` from `rest_framework_simplejwt.tokens` for creating JWT tokens.

This file provides a utility function for generating JWT tokens, which are used for user authentication and authorization in the application.
"""

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
