# This environment variable needs to be set first as channels uses it
import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.productionsettings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
import groupchat.routing
from groupchat.models import TokenAuthMiddlewareStack


from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            groupchat.routing.websocket_urlpatterns,
        )
    ),
})
