import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rankify_project.settings')

import django
import random
django.setup()


from rankify.models import Playlist, Song
from django.db import models
from django.contrib.auth.models import User
from rankify.spotify_utils import *


#NOTE: the population script uses real spotify user so that functionality
# such as their profile picture exists. However we don't use real playlist and
# song data because it would take to long to access the SpotifyAPI for all that
# data at once in the population script. Just using made up fake playlist data
# here


def populate():
    usernames = ['lewisrenfrew', 'alicejanehughes',
    'fizzgerald',  'ciaranroy1',
    'johnwise123', 'christopherjamesharkins', 'hemadeit']
    users = []

    # create users, use real spotify users so we have pics and links
    for username in usernames:
            user = User.objects.get_or_create(
                        username=username,
                        email= username + '@mydomain.com',
                        password='hashedPasswordStringPastedHere!',
                        is_active=True,
                        )[0]

            users.append(user)
            user.save()





    #lets add a few fake songs to the db, with fake danceabilities
    songs = []
    count = 1;

    for i in range(1, 100):
        song = Song.objects.get_or_create(
        song_name = 'song%d' % count,
        spotify_song_uri = 'spotify/song%d' % count,
        danceability = random.uniform(0, 1),
        )[0]
        songs.append(song)
        song.save()

        count = count + 1






    # create some fake playlists, one per users, add some songs, fudge the avgDanceability
    count = 1;
    up_to_song = 0



    for user in users:
        # songs we will add to this playlist, the next ten in the list of 100 songs
        my_songs = []
        total_danceability = 0;

        for i in range (up_to_song, up_to_song + 10): #0 to ten, ten to twent etc..
            my_songs.append(songs[i])
            total_danceability = total_danceability + songs[i].danceability

        display_name = get_display_name(user.username)
        if display_name:
            creator_name = display_name
        else:
            creator_name = user.username

        playlist = Playlist.objects.get_or_create(
        creator = user,
        creator_display_name = creator_name,
        playlist_image_url = get_profile_picture(user.username),
        name = 'playlist%d' % count,
        spotify_playlist_uri = 'spotify/playlist%d' % count,
        avg_danceability = total_danceability/10)[0]

        for song in my_songs:
            playlist.songs.add(song)



        playlist.save()
        up_to_song = up_to_song + 10
        count = count + 1









# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script... please wait...")
    populate()
