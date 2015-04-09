from django.conf.urls import patterns, url
from haircuttweets import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^search/$', views.search, name='search'),
	url(r'^trends/$', views.trends, name='trends'),
	url(r'^trunc/$', views.trunc, name='trunc'),

	)