from __future__ import print_function    # (at top of module)

import spotipy
import spotipy.util
from spotipy import util, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from texttable import Texttable
import urllib.request
from rankify.models import Song

from spotipy.oauth2 import SpotifyClientCredentials



import json

import time
import sys

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT=8000
CLIENT_ID='2af2fa2dd9c147f886a7b67c3d4ca031',
CLIENT_SECRET='562e93edd67b40cca215c3c882dc41a2'
REDIRECT_URI =  "{}:{}/rankify/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private"

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










# processes a users playlist track by track, adding each track to the db as a song
def get_tracks(playlist, username):
    songs = []
    try:
        results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
        tracks = results['tracks']

        for i, item in enumerate(tracks['items']):
            try: # none of this will work if spotify have removed/lost rights to the track
                track = item['track']
                features = sp.audio_features(track['id'])
                name = track['name']
                #print("the track is called ", name)
                uri = track['uri']
                #print("the track is at ", uri)

                #features is normally a list of features for multiple tracks
                #but since we are going through the list one by one it'll just have one
                #elements, i.e. features[0]
                thisTracksFeatures = features[0]
                danceability = thisTracksFeatures['danceability']
                #print("the track has a danceability of", danceability)



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

    except SpotifyException:
            print("playlist not found")

    return songs # return the list of songs


def get_display_name(username):
    user = sp.user(username)
    return user['display_name']


def get_profile_picture(username):
    user = sp.user(username)
    #print(user)
    pics = user['images']
    if pics:
        return pics[0]['url']
    else:
        return 'no picture set!!' #TODO - handle this with a default pic
