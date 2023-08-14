import os

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from core.shared.websockets import CORSAllowedOriginValidator

from rooms import routing
from rooms.middleware import SesameTokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': CORSAllowedOriginValidator(
        SesameTokenAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    )
})
