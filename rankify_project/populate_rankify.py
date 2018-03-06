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
    r_users = []
    count = 1;

    for test_user in users:
        r_user = UserProfile.objects.get_or_create(
        user = test_user,
        spotify_username = 'spotifyusername%d' % count,
        spotify_user_uri = 'spotify/user%d' % count,)[0]

        r_user.save()
        r_users.append(r_user)
        count = count + 1



    #lets add a few songs to the db
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



    for user_profile in r_users:
        # songs we will add to this playlist, the next ten in the list of 100 songs
        my_songs = []
        total_danceability = 0;

        for i in range (up_to_song, up_to_song + 10): #0 to ten, ten to twent etc..
            my_songs.append(songs[i])
            total_danceability = total_danceability + songs[i].danceability


        playlist = Playlist.objects.get_or_create(creator = user_profile,
        name = 'playlist%d' % count, spotify_playlist_uri = 'spotify/playlist%d' % count,
        avg_danceability = total_danceability/10)[0]

        for song in my_songs:
            playlist.songs.add(song)



        playlist.save()
        up_to_song = up_to_song + 10
        count = count + 1









# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
