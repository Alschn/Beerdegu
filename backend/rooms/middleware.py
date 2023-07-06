from typing import Callable

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from sesame.utils import get_user as sesame_get_user


@database_sync_to_async
def get_user_by_jwt(token: str | None):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser

    if not token:
        return AnonymousUser()

    User = get_user_model()

    try:
        decoded_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.SIMPLE_JWT['ALGORITHM']]
        )
        user_id = decoded_jwt.get(settings.SIMPLE_JWT['USER_ID_CLAIM'])

    except (
        jwt.exceptions.DecodeError,
        jwt.exceptions.InvalidTokenError,
        jwt.exceptions.InvalidSignatureError
    ):
        return AnonymousUser()

    if not user_id:
        return AnonymousUser()

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    query_string_key = 'token'

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string']

        try:
            query_string = query_string.decode()
            params = query_string.split('&')
            params_as_dict = dict(param.split('=') for param in params)
            token = params_as_dict.get(self.query_string_key, None)
        except ValueError:
            token = None

        scope['user'] = await get_user_by_jwt(token)
        return await super().__call__(scope, receive, send)


@database_sync_to_async
def get_user_by_sesame_token(token: str | None, ws_path: str):
    from django.contrib.auth.models import AnonymousUser

    if not token:
        return AnonymousUser()

    token_scope = ''
    if ws_path.startswith('/ws/room/'):
        _, room_name = ws_path.split('/ws/room/')
        room_name = room_name.replace('/', '')
        token_scope = f'rooms:{room_name}'

    user = sesame_get_user(
        token,
        scope=token_scope,
        update_last_login=False
    )

    if not user:
        return AnonymousUser()

    return user


class SesameTokenAuthMiddleware(BaseMiddleware):
    """
    Middleware for authenticating users via sesame token dedicated to websockets connections.
    Thanks to this approach, there is no need to send JWT token in query string.
    """
    query_string_key = 'token'

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        path = scope['path']
        query_string = scope['query_string']

        try:
            query_string = query_string.decode()
            params = query_string.split('&')
            params_as_dict = dict(param.split('=') for param in params)
            token = params_as_dict.get(self.query_string_key, None)
        except ValueError:
            token = None

        scope['user'] = await get_user_by_sesame_token(token, ws_path=path)
        return await super().__call__(scope, receive, send)
