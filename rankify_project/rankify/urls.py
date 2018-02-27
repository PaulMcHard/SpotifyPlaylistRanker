from django.conf.urls import url
from rankify import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rankings/$', views.rankings, name='rankings'),
    # just a placeholder for now, will change to specific user
    url(r'^user/$', views.user, name='user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^callback/$', views.callback, name='callback'),
]
