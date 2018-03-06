from __future__ import print_function    # (at top of module)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from texttable import Texttable

from rankify.models import Song



import json

import time
import sys


auth = oauth2.SpotifyClientCredentials(
    client_id='2af2fa2dd9c147f886a7b67c3d4ca031',
    client_secret='562e93edd67b40cca215c3c882dc41a2'
)

token = auth.get_access_token()
sp = spotipy.Spotify(auth=token)

# returns a list of all playlist objects for specified user
def get_playlists_by_username(spotify_username):
    playlists = sp.user_playlists(spotify_username)
    return playlists





# returns a list of the names (strings) of playlists created by this user
def get_playlist_names(username):
    playlists = sp.user_playlists(username)
    playlist_names = []

    for playlist in playlists['items']:

        # we only want to show playlists created by this user
        # i.e. not other users playlists they have saved to their profile
        # so they can only choose their own playlists
        if (playlist['owner']['id'] == username):
            playlist_names.append(playlist['name'])


    return playlist_names




# processes a users playlist track by track, adding each track to the db as a song
def get_tracks(playlist, username):
    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
    tracks = results['tracks']
    songs = []
    for i, item in enumerate(tracks['items']):
            try: # none of this will work if spotify have removed/lost rights to the track
                track = item['track']
                features = sp.audio_features(track['id'])
                name = track['name']
                print("the track is called ", name)
                uri = track['uri']
                print("the track is at ", uri)

                #features is normally a list of features for multiple tracks
                #but since we are going through the list one by one it'll just have one
                #elements, i.e. features[0]
                thisTracksFeatures = features[0]
                danceability = thisTracksFeatures['danceability']
                print("the track has a danceability of", danceability)



                # create a Song object and add it to the db with the info gathered so far
                song = Song.objects.get_or_create(
                song_name = name,
                spotify_song_uri = uri,
                danceability =  danceability,
                )[0]


                song.save() # save it to the db
                songs.append(song) # add it to the list

            except TypeError:
                print("spotify have removed this track")

    return songs # return the list of songs
