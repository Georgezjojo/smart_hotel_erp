import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import the URL patterns directly from the routing modules
from apps.operations.routing import websocket_urlpatterns as chat_ws
from apps.kitchen_display.routing import websocket_urlpatterns as kitchen_ws
from apps.realtime.routing import websocket_urlpatterns as realtime_ws

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_ws + kitchen_ws + realtime_ws
        )
    ),
})