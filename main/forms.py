from django.forms import ModelForm
from . import models

class PlayerForm(ModelForm):
	class Meta:
		model = models.Player
		fields = ['status', 'bio']
