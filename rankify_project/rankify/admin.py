from django.contrib import admin

from rankify.models import Playlist, Song, UserProfile

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'avgDanceability', 'spotifyPlaylistURI')


class SongAdmin(admin.ModelAdmin):
    list_display = ('songName', 'spotifySongURI', 'danceability')

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)
