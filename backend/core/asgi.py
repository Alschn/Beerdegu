import os

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from rooms import routing
from rooms.middleware import SesameTokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        SesameTokenAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    )
})
