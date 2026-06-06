import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()  # 👈 Must come first

# Now it's safe to import things that touch models
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.operations.routing import websocket_urlpatterns as chat_ws
from apps.kitchen_display.routing import websocket_urlpatterns as kitchen_ws  # if you have kitchen routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_ws + kitchen_ws   # combine your routing lists
        )
    ),
})