from django.db import models
from django.contrib.auth.models import User

# we'll need to include songs in our database too, since one of our
# requirements was to breakdown danceability song by song
# we could ask the spotify API every time, but that'd be slower I think
class Song(models.Model):
    #spotify assings all songs a uri, they are findable by this
    #including uris in the db makes it possible to add 'open in spotify'
    #functionalities for users profiles, songs and playlists, although we might
    #not have time to do that this time round
    spotify_song_uri = models.CharField(max_length=128,)
    song_name = models.CharField(max_length=128, unique=False)
    danceability = models.FloatField()




    def __str__(self):
        return self.song_name


class Playlist(models.Model):
    #spotify assings all polaylists a uri, they are findable by this
    spotify_playlist_uri = models.CharField(max_length=128,)
    # two playlists could have the same name, hence unique false
    name = models.CharField(max_length=128, unique=False,  null = False)
    avg_danceability = models.FloatField(default = 0)


    # we set up a one to many relationship between users and Playlists
    # i.e. one user has many Playlists
    # the cascade option means playlists go bye bye if creators UserProfile is deleted
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    # we set up a many to many relationship between playlists and songs
    songs = models.ManyToManyField(Song)




    def __str__(self):
        return self.name
