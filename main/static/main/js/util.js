"use strict";

function socket_send(s, tag, data) {
	s.send(JSON.stringify({
		'tag': tag,
		'data': data,
	}));
}
function distance(ll1, ll2) {
	var R2D = 180.0 / Math.PI;
	var D2R = Math.PI / 180.0;
	var R = 6371.0 * 1000;
	var lat_avg = (ll1.lat + ll2.lat) * D2R / 2;
	var z = Math.cos(lat_avg);
	var yd = ll2.lat * D2R - ll1.lat * D2R;
	var xd = (ll2.lon - ll1.lon) * D2R * z;
	return R * Math.sqrt(yd * yd + xd * xd);
}
