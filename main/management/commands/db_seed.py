from django.core.management.base import BaseCommand

from pprint import pprint

from django.contrib.auth.models import User
from main.models import *

class Command(BaseCommand):
	help = 'Seeds database.'

	def handle(self, *args, **options):
		print('Command db_seed.')
		print('Args are:')
		pprint(args)
		print('Options are:')
		pprint(options)
		print('---')
		print('Seeding database...')
		self.seed()

	def seed(self):
		admin = User.objects.get(username='admin')
		try:
			admin.player
			print('Database already seeded.')
		except Player.DoesNotExist:
			p = Player.create(admin)
			p.save()
			print('Seeded database.')
