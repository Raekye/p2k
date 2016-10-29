from django.conf.urls import url, include

from . import views

app_name = 'main'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^game/$', views.game, name='game'),
	url(r'^profile/(?P<uuid>[a-f0-9-]+)/$', views.profile, name='profile'),
	url('^accounts/edit/$', views.account, name='edit'),
	url('^accounts/', include('django.contrib.auth.urls')),
]
