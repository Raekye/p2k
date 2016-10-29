"use strict";

var world_socket = null;

function world_init() {
	world_socket = new WebSocket('ws://' + window.location.host + '/world/');
	world_socket.onmessage = world_recv;
}
function world_recv(d) {
	d = JSON.parse(d.data);
	if (d.tag == 'load') {
		map_reset();
		var centre = d.data.centre;
		var gcentre = { 'lat': centre.lat, 'lng': centre.lon };
		map.setCenter(gcentre);
		map_overlays.push(map_draw_circle(centre));
		map_draw_grid();
		world_load_entities(d.data.entities)
	} else if (d.tag == 'move') {
		if (d.id in history) {
			console.log("Already seen event", d.id);
		} else {
			console.log("Processing event", d.id);
			console.log(d);
			history[d.id] = true;
			world_move(global_entities[d.data.player], d.data.start, d.data.end);
		}
	}
}
function world_load_entities(entities) {
	console.log("Loading entities", entities);
	for (var k in entities.structures) {
		var s = entities.structures[k]
		console.log("Loading structure", s);
		if (s.tag == 1) {
			var m =new google.maps.Marker({
				position: { lat: s.pos.lat, lng: s.pos.lon },
				map: map,
				icon: new google.maps.MarkerImage(ICONS['tree'], new google.maps.Size(80, 128), new google.maps.Point(180, 0)),
			});
			map_overlays.push(m);
			world_update_visibility(m);
		}
	}
	for (var k in entities.players) {
		console.log("Loading player", k);
		global_entities[k] = new google.maps.Marker({
			position: {
				lat: entities.players[k].pos.lat,
				lng: entities.players[k].pos.lon,
			},
			zIndex: 1000,
			map: map,
			icon: new google.maps.MarkerImage(ICONS['avatar-0'], new google.maps.Size(32, 48), new google.maps.Point(0, 0), new google.maps.Point(16, 20)),
		});
		world_update_visibility(global_entities[k]);
	}
}
function world_send_recentre() {
	world_send('recentre', {});
}
function world_send_move(ll) {
	if (world_socket == null) {
		return;
	}
	var d = distance(banana(map.getCenter()), ll);
	console.log("Click coordinates", ll.lat, ll.lon, "distance", d);
	if (!world_is_in_range(ll)) {
		return;
	}
	world_send('move', {
		'target': {
			'lat': ll.lat,
			'lon': ll.lon,
		},
	});
}
function world_is_in_range(ll) {
	var d = distance(banana(map.getCenter()), ll);
	return d < 800;
}
function world_move(player, start, end) {
	console.log("Moving", player, start, end);
	clearInterval(movement);
	var t = end.t - start.t;
	var n = Math.round(t / 0.010);
	var dlat = (end.lat - start.lat) / n;
	var dlon = (end.lon - start.lon) / n;
	player.setPosition({
		'lat': start.lat,
		'lng': start.lon,
	});
	var i = 0;
	movement = setInterval(function () {
		if (i >= n) {
			clearInterval(movement);
			return;
		}
		var pos = banana(player.position);
		player.setPosition({
			'lat': pos.lat + dlat,
			'lng': pos.lon + dlon,
		});
		world_update_visibility(player);
		i++;
	}, 10);
}
function world_send(tag, data) {
	if (world_socket == null) {
		return;
	}
	socket_send(world_socket, tag, data);
}
function world_update_visibility(m) {
	return;
	if (world_is_in_range(banana(m.position))) {
		if (m.map == null) {
			m.setMap(map);
		}
	} else {
		if (m.map != null) {
			m.setMap(null);
		}
	}
}
