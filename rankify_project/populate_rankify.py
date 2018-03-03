import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rankify_project.settings')

import django
import random
django.setup()

from rankify.models import UserProfile
from rankify.models import Playlist, Song
from django.db import models
from django.contrib.auth.models import User





def populate():
    users = []

    # create 10 fake django user profiles, if theyre not there already
    for i in range(1, 10):
            user = User.objects.get_or_create(
                        username='user%d' % i,
                        email='user%d@mydomain.com' % i,
                        password='hashedPasswordStringPastedHere!',
                        is_active=True,
                        )[0]

            users.append(user)
            user.save()


    # now create 10 rankify specific UserProfiles, link them to the django user
    rUsers = []
    count = 1;

    for aUser in users:
        rUser = UserProfile.objects.get_or_create(
        user = aUser, spotifyUserURI = 'spotify/user%d' % count,)[0]
        rUser.save()
        rUsers.append(rUser)
        count = count + 1



    #lets add a few songs to the db
    songs = []
    count = 1;

    for i in range(1, 100):
        song = Song.objects.get_or_create(
        songName = 'song%d' % count,
        spotifySongURI = 'spotify/song%d' % count,
        danceability = random.uniform(0, 1),
        )[0]
        songs.append(song)
        song.save()

        count = count + 1






    # create some fake playlists, one per users, add some songs, fudge the avgDanceability
    count = 1;
    uptoSong = 0



    for userProfile in rUsers:
        # songs we will add to this playlist, the next ten in the list of 100 songs
        mySongs = []
        totalDanceability = 0;

        for i in range (uptoSong, uptoSong + 10): #0 to ten, ten to twent etc..
            mySongs.append(songs[i])
            totalDanceability = totalDanceability + songs[i].danceability


        playlist = Playlist.objects.get_or_create(creator = userProfile,
        name = 'playlist%d' % count, spotifyPlaylistURI = 'spotify/playlist%d' % count,
        avgDanceability = totalDanceability/10)[0]

        for song in mySongs:
            playlist.songs.add(song)



        playlist.save()
        uptoSong = uptoSong + 10
        count = count + 1









# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
