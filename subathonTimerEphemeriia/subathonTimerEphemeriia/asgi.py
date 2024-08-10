"""
ASGI config for subathonTimerEphemeriia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import subathonTimer.routing as routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subathonTimerEphemeriia.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "https": django_asgi_app,
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    )
})
