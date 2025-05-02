from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token  # need to replace with JWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs


# # need to review with JWTAuthentication implementation
# @database_sync_to_async
# def get_user(token_key):
#     try:
#         token = Token.objects.get(key=token_key)
#         return token.user
#     except Token.DoesNotExist:
#         return AnonymousUser()
#
#
# class TokenAuthMiddleware(BaseMiddleware):
#
#     def __init__(self, inner):
#         self.inner = inner
#
#     async def __call__(self, scope, receive, send):
#         headers = dict(scope['headers'])
#         if b'authorization' in headers:
#             token_name, token_key = headers[b'authorization'].decode().split()
#             if token_name == 'Token':
#                 scope['user'] = await get_user(token_key)
#         return await super().__call__(scope, receive, send)

@database_sync_to_async
def get_user_from_jwt(token):
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user
    except (InvalidToken, TokenError) as e:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        token = None

        # Authorization: Bearer <token>
        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode()
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # Optional fallback: use token from query string
        if not token:
            query_string = scope.get("query_string", b"").decode()
            token = parse_qs(query_string).get("token", [None])[0]

        # Authenticate the user if token found
        if token:
            scope["user"] = await get_user_from_jwt(token)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
