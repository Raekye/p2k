from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from . import forms

# Create your views here.

def index(req):
	return render(req, 'main/index.html', {
		'ucf': UserCreationForm(),
	})

@login_required
def game(req):
	return render(req, 'main/game.html', {
		'google_maps_key': settings.GOOGLE_MAPS_KEY,
	})

@login_required
def account(req):
	return render(req, 'main/account.html', {
		'form': forms.PlayerForm(),
	})

def profile(req, uuid):
	return render(req, 'main/profile.html', {
		'uuid': uuid,
	})
