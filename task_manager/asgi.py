import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import src.apps.tasks.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(src.apps.tasks.routing.websocket_urlpatterns)
        ),
    }
)
