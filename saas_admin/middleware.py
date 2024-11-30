# middleware.py
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract the token from the query string
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("query_string")
        # print(token)

        if token:
            try:
                # Decode the token and fetch the user
                payload = jwt.decode(
                    token[0], settings.SECRET_KEY, algorithms=["HS256"]
                )
                user_id = payload.get("user_id")
                scope["user"] = await get_user(user_id)
            except jwt.ExpiredSignatureError:
                scope["user"] = AnonymousUser()
            except jwt.InvalidTokenError:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
