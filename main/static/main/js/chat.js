"use strict";

var chat_socket = null;

function chat_init() {
	chat_socket = new WebSocket('ws://' + window.location.host + '/chat/');
	chat_socket.onmessage = chat_recv;
}
function chat_send(room, msg) {
	socket_send(chat_socket, 'send', {
		'room': room,
		'msg': msg,
	});
}
function chat_subscribe(room, yes) {
	socket_send(chat_socket, 'subscribe', {
		'room': room,
		'yes': yes,
	});
}
function chat_recv(d) {
	var data = JSON.parse(d.data);
	console.log(data);
}
