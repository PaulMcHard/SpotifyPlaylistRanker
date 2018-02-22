from django.contrib import admin

from rankify.models import Playlist, Song, User

admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(User)
