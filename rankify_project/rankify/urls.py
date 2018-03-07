from django.conf.urls import url
from rankify import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT=8000



LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rankings/$', views.rankings, name='rankings'),
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),

    # just a placeholder for now, will change to specific user
    url(r'^user/$', views.user, name='user'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),



    
]
