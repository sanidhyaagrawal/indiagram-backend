from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat_v1 import routing as v1_routing

application = ProtocolTypeRouter({
    "websocket": URLRouter(
            v1_routing.websocket_urlpatterns
            )
    
})
