from django.db import models
from django.contrib.auth.models import User














class UserProfile(models.Model):

    # This line is required. Links UserProfile to a User model instance.
    # note that we don't need explciit username field since its stored in user
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    # n.b Cascade deletes User 'user' if this User is deleted from db
    # confusing I know... see tango page 107: The User Model

    #I think password is an attribute of user too so not including it here
    # TODO - Lewis: check this

    #spotify assigns all users a uri. We'll tie this to a users account if
    #they upload a spotify playlist, defaults to none before that point
    spotifyUserURI = models.CharField(max_length=128, unique=True, default=None)

    # profile picture, will be chosen by the user when they sign up
    # profile images will live in media/profile_images
    picture = models.ImageField(upload_to='profile_images', blank=True)



    def __str__(self):
        return self.user.username








# we'll need to include songs in our database too, since one of our
# requirements was to breakdown danceability song by song
# we could ask the spotify API every time, but that'd be slower I think
class Song(models.Model):
    #spotify assings all songs a uri, they are findable by this
    spotifySongURI = models.CharField(max_length=128, unique=True)
    songName = models.CharField(max_length=128, unique=True)
    danceability = models.FloatField()



    def __str__(self):
        return self.songName




class Playlist(models.Model):
    #spotify assings all polaylists a uri, they are findable by this
    spotifyPlaylistURI = models.CharField(max_length=128, unique=True,)
    name = models.CharField(max_length=128, unique=True,  null = False)
    avgDanceability = models.FloatField(null = True) # TODO Lewis null?


    # we set up a one to many relationship between users and Playlists
    # i.e. one user has many Playlists
    # the cascade option means playlists go bye bye if user is deleted
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # we set up a many to many relationship between playlists and songs
    songs = models.ManyToManyField(Song)




    def __str__(self):
        return self.name
