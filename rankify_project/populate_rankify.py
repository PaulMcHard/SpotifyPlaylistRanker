import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rankify_project.settings')

import django
import random
django.setup()


from rankify.models import Playlist, Song
from django.db import models
from django.contrib.auth.models import User
from rankify.spotify_utils import get_playlists_by_username, get_tracks





def populate():
    users = []
    usernames = ['werfner', 'conandhez', 'alicejanehughes', '1149261502' ]
    # pick some short playlists of these users to quickly add to the db
    sample_playlist_names = ['pizza', 'spring', 'hype',
    'Palm Trees & Conrete', 'berlin winter', 'u know i know', 'fresh creps', 'stuff to hear'  ]

    # create 10 fake django user profiles, if theyre not there already
    counter = 0
    for username in usernames:
            user = User.objects.get_or_create(
                        username=usernames[counter],
                        password='hashedPasswordStringPastedHere!',
                        )[0]

            users.append(user)
            user.save()
            counter += 1















    for the_user in users:
        # songs we will add to this playlist, the next ten in the list of 100 songs
        #print('in user loop')

        playlists = get_playlists_by_username(the_user.username)

        #search this users playlists till we find which one was selected
        for playlist in playlists['items']:
            #print('in plist loop')
            if playlist['name'] in sample_playlist_names:
                if (playlist['owner']['id'] == the_user.username):


                    print(playlist['name'])

                    our_playlist = Playlist.objects.get_or_create(
                    name = playlist['name'],
                    creator = User.objects.get(username = the_user.username),
                    spotify_playlist_uri = playlist['uri']
                    )[0]
                    our_playlist.save()



                    total_danceability = 0
                    track_counter = 0


                        #the get_tracks function does a lot...
                        #it gets tracks from the playlist and adds them to the db as Songs
                        # and returns a list of songs
                    songs = get_tracks(playlist, the_user.username)

                        #add every song in the list to the playlist entry in the db
                    for song in songs:
                        #print('in song loop')
                        our_playlist.songs.add(song)
                        total_danceability += song.danceability
                        track_counter += 1

                        # add the playlists uri to the db

                        #add the playlists danceability!
                    if track_counter > 0:
                        avg_danceability = total_danceability / track_counter
                        our_playlist.avg_danceability = avg_danceability
                        avg_danceability = round(  avg_danceability, 2 )




                    our_playlist.save() #and save the playlist













# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
