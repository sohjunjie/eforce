from channels.routing import route
from sw_layer.consumers import ws_connect_efhq, ws_connect_efassets, ws_disconnect_hq, ws_disconnect_efassets


channel_routing = [
    route("websocket.connect", ws_connect_efhq, path=r'^/efhq/$'),

    route("websocket.connect", ws_connect_efassets, path=r'^/efassets/$'),

    route("websocket.disconnect", ws_disconnect_hq, path=r'^/efhq/$'),
    route("websocket.disconnect", ws_disconnect_efassets, path=r'^/efassets/$'),


]
