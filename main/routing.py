from channels.routing import route, route_class

from . import consumers

channel_routing = [
	route('websocket.connect', consumers.chat_connect, path=r'^/chat/$'),
	route('websocket.receive', consumers.chat_receive, path=r'^/chat/$'),
	route('websocket.disconnect', consumers.chat_disconnect, path=r'^/chat/$'),
	route('websocket.connect', consumers.world_connect, path=r'^/world/$'),
	route('websocket.receive', consumers.world_receive, path=r'^/world/$'),
	route('websocket.disconnect', consumers.world_disconnect, path=r'^/world/$'),
]
