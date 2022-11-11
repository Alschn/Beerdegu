import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings


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

    except jwt.exceptions.DecodeError:
        return AnonymousUser()

    except jwt.exceptions.ExpiredSignatureError:
        return AnonymousUser()

    try:
        return AnonymousUser() if user_id is None else User.objects.get(id=user_id)

    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None

        scope['user'] = await get_user_by_jwt(token_key)
        return await super().__call__(scope, receive, send)
