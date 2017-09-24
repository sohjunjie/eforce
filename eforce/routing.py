from channels.routing import route
from sw_layer.consumers import ws_message


channel_routing = [
    route("websocket.receive", ws_message),
]
