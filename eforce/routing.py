from channels.routing import route

from sw_layer.consumers import ws_connect_efhq, ws_connect_efassets, ws_disconnect_hq, \
    ws_disconnect_efassets

# FOR AIRLINEAPP
from sw_layer.consumers import ws_connect_airlinechat, ws_disconnect_airlinechat, \
    ws_receive_airlinechat

channel_routing = [
    route("websocket.connect", ws_connect_efhq, path=r'^/efhq/$'),
    route("websocket.connect", ws_connect_efassets, path=r'^/efassets/$'),
    route("websocket.disconnect", ws_disconnect_hq, path=r'^/efhq/$'),
    route("websocket.disconnect", ws_disconnect_efassets, path=r'^/efassets/$'),


    # FOR AIRLINEAPP
    route("websocket.connect", ws_connect_airlinechat, path=r'^/airlineapp/chat/$'),
    route("websocket.receive", ws_receive_airlinechat, path=r'^/airlineapp/chat/$'),
    route("websocket.disconnect", ws_disconnect_airlinechat, path=r'^/airlineapp/chat/$'),

]
