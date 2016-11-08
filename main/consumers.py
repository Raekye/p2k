from channels import Group, Channel
from channels.generic.websockets import WebsocketConsumer
from channels.auth import channel_session_user_from_http, channel_session_user

import json
import uuid
from pprint import pprint

from django.core.cache import caches
from . import models

cache = caches['default']

@channel_session_user_from_http
def chat_connect(msg):
	pass

@channel_session_user
def chat_receive(msg):
	if not msg.user.is_authenticated():
		# TODO
		return
	data = json.loads(msg.content['text'])
	pprint(data)
	tag = data['tag']
	room = data['data']['room']
	group = Group('chat-' + room)
	if tag == 'send':
		group.add(msg.reply_channel)
		group.send({
			'text': json.dumps({
				'user': msg.user.player.id,
				'room': room,
				'msg': data['data']['msg'],
			}),
		})
	elif tag == 'subscribe':
		if data['data']['yes']:
			group.add(msg.reply_channel)
		else:
			group.discard(msg.reply_channel)

@channel_session_user
def chat_disconnect(msg):
	pass

@channel_session_user_from_http
def world_connect(msg):
	pprint(msg.user)
	if not msg.user.is_authenticated():
		# TODO
		return
	world_send_load(msg, msg.user.player)

@channel_session_user
def world_receive(msg):
	pprint(msg.user)
	if not msg.user.is_authenticated():
		# TODO
		return
	pprint(msg.content)
	p = msg.user.player
	data = json.loads(msg.content['text'])
	pprint(data)
	if data['tag'] == 'move':
		target_lat = data['data']['target']['lat']
		target_lon = data['data']['target']['lon']
		m = p.motion()
		m.move(target_lat, target_lon)
		m.save()
		if p.can_move_to(target_lat, target_lon):
			pprint(msg.channel_session['chunks'])
			event_id = str(uuid.uuid4())
			for c in msg.channel_session['chunks']:
				c = models.Chunk(c)
				Group('chunk-' + c.to_key()).send({
					'text': json.dumps({
						'id': event_id,
						'tag': 'move',
						'data': {
							'player': str(p.id),
							'start': {
								'lat': m.lat,
								'lon': m.lon,
								't': m.t1,
							},
							'end': {
								'lat': m.lat2,
								'lon': m.lon2,
								't': m.t2,
							},
						},
					}),
				})
	elif data['tag'] == 'recentre':
		m = p.motion()
		m.recenter()
		m.cancel()
		p.centre_lat = m.lat
		p.centre_lon = m.lon
		p.lat = m.lat
		p.lon = m.lon
		p.save()
		world_send_load(msg, p)

@channel_session_user
def world_disconnect(msg):
	if not msg.user.is_authenticated():
		# TODO
		return
	# TODO: remove from chunk, save data

def world_send_load(msg, p):
	chunks = models.Chunk.chunks_for_centre(p.centre_lat, p.centre_lon)
	if 'chunks' in msg.channel_session:
		print('Discarding chunks')
		for c in msg.channel_session['chunks']:
			Group('chunk-' + models.Chunk(c).to_key()).discard(msg.reply_channel)
	msg.channel_session['chunks'] = list(chunks)
	entities = {
		'players': {},
		'structures': {},
	}
	for c in chunks:
		c.load(entities)
		Group('chunk-' + c.to_key()).add(msg.reply_channel)
	#pprint(entities)
	msg.reply_channel.send({
		'text': json.dumps({
			'tag': 'load',
			'data': {
				'centre': {
					'lat': p.centre_lat,
					'lon': p.centre_lon,
				},
				'pos': {
					'lat': p.lat,
					'lon': p.lon,
				},
				'entities': entities,
			},
		}),
	})
