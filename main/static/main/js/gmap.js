"use strict";

var map = null;
var map_overlays = [];

var global_entities = {};
var event_history = {};
var movement = null;

function banana(ll) {
	return {
		'lat': ll.lat(),
		'lon': ll.lng(),
	};
}
function map_init() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: { lat: 0, lng: 0 },
		zoom: 16,
		//minZoom: 16,
		maxZoom: 16,
		disableDefaultUI: true,
		clickableIcons: false,
		draggableCursor: 'pointer',
	});

	google.maps.event.addListener(map, "click", function (e) {
		world_send_move(banana(e.latLng));
	});

	chat_init();
	world_init();
}
function map_draw_grid() {
	var centre = banana(map.getCenter())
	var lat_snap = Math.floor(centre.lat * 100);
	var lon_snap = Math.floor(centre.lon * 100);
	var n = (lat_snap + 4) / 100.0;
	var s = (lat_snap - 4) / 100.0;
	var w = (lon_snap - 4) / 100.0;
	var e = (lon_snap + 4) / 100.0;
	for (var i = 0; i < 9; i++) {
		var lat = (lat_snap + i - 4) / 100.0;
		var lon = (lon_snap + i - 4) / 100.0;
		map_overlays.push(new google.maps.Polyline({
			path: [
				{ lat: lat, lng: e },
				{ lat: lat, lng: w },
			],
			map: map,
		}));
		map_overlays.push(new google.maps.Polyline({
			path: [
				{ lat: n, lng: lon },
				{ lat: s, lng: lon },
			],
			map: map,
		}));
	}
}
function map_reset() {
	for (let o of map_overlays) {
		o.setMap(null);
	}
	for (var k in global_entities) {
		global_entities[k].setMap(null);
	}
	map_overlays = [];
	global_entities = {};
}
function map_generate_circle(centre, radius) {
	var R2D = 180.0 / Math.PI;
	var D2R = Math.PI / 180.0;
	var R = 6371.0 * 1000;
	var N = 64;
	var z = Math.cos(centre.lat * D2R);
	var rlat = radius / R * R2D;
	var rlon = rlat / z;
	var bounds = [];
	for (var i = 0; i < N; i++) {
		var rad = i * 2 * Math.PI / N;
		var x = centre.lon + rlon * Math.cos(rad);
		var y = centre.lat + rlat * Math.sin(rad);
		bounds.push(new google.maps.LatLng(y, x));
	}
	bounds.push(bounds[0]);
	return bounds;
}
function map_draw_circle(centre) {
	return new google.maps.Polyline({
		path: map_generate_circle(centre, 800),
		strokeOpacity: 0,
		icons: [{
			icon: {
				path: 'M 0, -1 0, 1',
				strokeOpacity: 1,
				scale: 4,
			},
			offset: '0',
			repeat: '20px',
		}],
		map: map,
		clickable: false,
	});
	/*
	return new google.maps.Circle({
		strokeColor: '#FF0000',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#FF0000',
		fillOpacity: 0.35,
		map: map,
		center: centre,
		radius: 800,
		clickable: false,
	});
	*/
}
