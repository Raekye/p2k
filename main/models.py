from django.db import models
from django.conf import settings
from django.core.cache import caches

import math
import time
import uuid
import random
import datetime
from pprint import pprint

# Create your models here.

class BaseModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='ID')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Player(BaseModel):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
	city = models.ForeignKey('City', null=True, related_name='members')
	clan = models.ForeignKey('Clan', null=True, related_name='members')

	hp = models.IntegerField()
	avatar = models.IntegerField()
	gold = models.IntegerField()

	centre_lat = models.FloatField()
	centre_lon = models.FloatField()
	pos_lat = models.FloatField()
	pos_lon = models.FloatField()

	status = models.CharField(max_length=64)
	bio = models.CharField(max_length=256)

	def can_move_to(self, lat, lon):
		return Chunk.distance(self.centre_lat, self.centre_lon, lat, lon) < 800

	def player_position(self):
		return PlayerPosition.cache.get_or_set('player-pos.' + str(self.id), PlayerPosition(self), 3600)

	@staticmethod
	def effective_level(l):
		return sum([x ** (1 + 0.5 * math.exp(-i)) for (i, x) in enumerate(l)]) / len(l)

	@staticmethod
	def create(u):
		lat = -34.397
		lon = 150.644
		return Player(user=u, hp=100, avatar=0, gold=100, centre_lat=lat, centre_lon=lon, pos_lat=lat, pos_lon=lon)

class ItemModel(BaseModel):
	tag = models.IntegerField()
	quantity = models.IntegerField()
	metadata = models.BinaryField()

	class Meta:
		abstract = True

class Structure(BaseModel):
	tag = models.IntegerField()
	hp = models.IntegerField()
	metadata = models.BinaryField()
	lat = models.FloatField()
	lon = models.FloatField()

class NatureStructure(Structure):
	last_harvest = models.DateTimeField()

class PlayerStructure(Structure):
	creator = models.ForeignKey(Player, models.CASCADE)

class Flag(PlayerStructure):
	level = models.IntegerField()
	availability = models.IntegerField()
	fee = models.IntegerField()

class City(PlayerStructure):
	major = models.OneToOneField(Player, models.CASCADE, null=True, related_name='lead_cities')

	name = models.CharField(max_length=32)

class TradePost(PlayerStructure):
	corresponding_city = models.OneToOneField(City, models.CASCADE, related_name='city2')

class CityFlag(Structure):
	city = models.ForeignKey(City, models.CASCADE)

	level = models.IntegerField()

class Library(PlayerStructure):
	fee = models.IntegerField()
	skill = models.IntegerField()
	level = models.IntegerField()

class FlagPass(BaseModel):
	builder = models.ForeignKey(Player, models.CASCADE, related_name='flag_passes_given')
	license = models.ForeignKey(Player, models.CASCADE, related_name='flag_passes_received')

class Clan(BaseModel):
	leader = models.OneToOneField(Player, models.CASCADE, related_name='clan_lead')

	name = models.CharField(max_length=32)

class Skill(BaseModel):
	player = models.ForeignKey(Player, models.CASCADE)

	tag = models.IntegerField()
	transient_exp = models.IntegerField()
	total_exp = models.IntegerField()

class TradePostListing(ItemModel):
	tradepost = models.ForeignKey(TradePost, models.CASCADE)

class PlayerItem(ItemModel):
	player = models.ForeignKey(Player, models.CASCADE, related_name='inventory')

class GroundItem(ItemModel):
	lat = models.FloatField()
	lon = models.FloatField()

# Non Django
class Chunk(tuple):
	cache = caches['default']
	GRANULARITY = 100.0

	def __new__(cls, ll):
		return super(Chunk, cls).__new__(cls, ll)

	def load(self, entities):
		if Chunk.cache.add('chunk-' + self.to_key(), True, 15):
			print('Generating')
			self.generate()
		else:
			print('Already generated')
		s = self[0] / Chunk.GRANULARITY
		w = self[1] / Chunk.GRANULARITY
		n = (self[0] + 1) / Chunk.GRANULARITY
		e = (self[1] + 1) / Chunk.GRANULARITY
		players = Player.objects.filter(pos_lat__gte=s, pos_lat__lt=n, pos_lon__gte=w, pos_lon__lt=e)
		for p in players:
			print(p.user.username + ", " + str(p.id))
		structures = self.get_structures()
		for p in players:
			pp = p.player_position()
			pp.recenter()
			entities['players'][str(p.id)] = {
				'username': p.user.username,
				'pos': {
					'lat': pp.lat,
					'lon': pp.lon,
				},
			}
		for s in structures:
			entities['structures'][str(s.id)] = {
				'tag': s.tag,
				'pos': {
					'lat': s.lat,
					'lon': s.lon,
				},
			}

	def get_structures(self):
		s = self[0] / Chunk.GRANULARITY
		w = self[1] / Chunk.GRANULARITY
		n = (self[0] + 1) / Chunk.GRANULARITY
		e = (self[1] + 1) / Chunk.GRANULARITY
		return Structure.objects.filter(lat__gte=s, lat__lt=n, lon__gte=w, lon__lt=e)

	def generate(self):
		structures = self.get_structures()
		num = random.randint(4, 16)
		print('num is ' + str(num) + ', count is ' + str(structures.count()))
		if structures.count() < num:
			structures = list(structures)
			for i in range(len(structures), num):
				lat = (random.random() + self[0]) / Chunk.GRANULARITY
				lon = (random.random() + self[1]) / Chunk.GRANULARITY
				badness = False
				for y in structures:
					d = Chunk.distance(lat, lon, y.lat, y.lon)
					if d < 200:
						badness = True
						break
				if badness:
					continue
				x = NatureStructure(lat=lat, lon=lon, hp=20, tag=1, last_harvest=datetime.datetime.now())
				x.save()
				structures.append(x)


	def to_key(self):
		return str(self[0]) + '_' + str(self[1])

	@staticmethod
	def from_key(s):
		parts = s.split('_')
		assert(len(parts) == 2)
		return Chunk(map(int, parts))

	@staticmethod
	def get(lat, lon):
		return Chunk(Chunk.lower_left_corner(lat, lon))

	@staticmethod
	def chunks_for_centre(lat, lon):
		(n, s, w, e) = Chunk.bounding_box_for_circle(lat, lon)
		#print(str(n) + ", " + str(s) + ", " + str(w) + ", " + str(e))
		return Chunk.closure(Chunk.get(s, w), Chunk.get(n, e))

	@staticmethod
	def closure(sw, ne):
		pprint(sw)
		pprint(ne)
		ret = set()
		for y in range(sw[0], ne[0] + 1):
			for x in range(sw[1], ne[1] + 1):
				ret.add(Chunk((y, x)))
		pprint(ret)
		return ret


	@staticmethod
	def lower_left_corner(lat, lon):
		assert(lat < 86)
		assert(lat > -86)
		assert(lon < 360)
		assert(lon > -360)
		ROUND_TO_INVERSE = 1000 / 10
		if lat > 85:
			lat = 85
		elif lat < -85:
			lat = -85
		lon = (lon + 180) % 360 - 180
		lat2 = math.floor(lat * ROUND_TO_INVERSE)
		lon2 = math.floor(lon * ROUND_TO_INVERSE)
		return (lat2, lon2)

	@staticmethod
	def bounding_box_for_circle(lat, lon):
		D2R = math.pi / 180.0
		R2D = 180.0 / math.pi
		EARTH_RADIUS = 6.371e6
		d = 850.0
		# for radians
		# d^2 = (y2 - y1)^2 + (x2 - x1)^2
		# y = R * lat
		# x = R * lon * cos(lat)
		k = d / EARTH_RADIUS
		lat2 = lat * D2R
		z = math.cos(lat2)
		lon2 = lon * z * D2R
		return ((lat2 + k) * R2D, (lat2 - k) * R2D, (lon2 - k) * R2D / z, (lon2 + k) * R2D / z)

	@staticmethod
	def distance(lat1, lon1, lat2, lon2):
		D2R = math.pi / 180.0
		R2D = 180.0 / math.pi
		EARTH_RADIUS = 6.371e6
		lat1 = lat1 * D2R
		lat2 = lat2 * D2R
		z = math.cos((lat1 + lat2) / 2)
		yd = lat2 - lat1
		xd = (lon2 - lon1) * D2R * z
		return EARTH_RADIUS * math.sqrt(yd * yd + xd * xd)

class PlayerPosition(object):
	cache = caches['default']

	def __init__(self, p):
		self.player = p.id
		self.lat2 = p.pos_lat
		self.lon2 = p.pos_lon
		self.t1 = 0
		self.t2 = 0

	def recenter(self):
		now = time.time()
		if now < self.t2:
			fraction = (now - self.t1) / (self.t2 - self.t1)
			self.lat += (self.lat2 - self.lat) * fraction
			self.lon += (self.lon2 - self.lon) * fraction
			self.t1 = now
		else:
			self.lat = self.lat2
			self.lon = self.lon2

	def cancel(self):
		self.t2 = 0

	def move(self, lat2, lon2):
		self.recenter()
		d = Chunk.distance(self.lat, self.lon, lat2, lon2)
		t = d / (1600.0 / 5)
		self.t1 = time.time()
		self.t2 = self.t1 + t
		self.lat2 = lat2
		self.lon2 = lon2

	def save(self):
		PlayerPosition.cache.set('player-pos.' + str(self.player), self, 3600)
