from django.conf.urls import url
from rankify import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rankings/$', views.rankings, name='rankings'),
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),
    url(r'^link_spotify/$', views.link_spotify, name='link_spotify'),
    url(r'^callback/$', views.callback, name='callback'),
    # just a placeholder for now, will change to specific user
    url(r'^user/$', views.user, name='user'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^register/$', views.register, name='register'),
]
