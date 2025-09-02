# """
# ASGI config for Yasla project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
# """

# import os
# import django
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import App1.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yasla.settings')
# django.setup()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             App1.routing.websocket_urlpatterns
#         )
#     ),
# })


# project_name/asgi.py
import os
from django.core.asgi import get_asgi_application   # <-- import it here
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from App1.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Yasla.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

