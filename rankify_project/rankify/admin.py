from django.contrib import admin
from rankify.models import Playlist, Song

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'avg_danceability', 'spotify_playlist_uri')


class SongAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'spotify_song_uri', 'danceability')

    
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
