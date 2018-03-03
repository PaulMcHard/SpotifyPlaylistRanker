from __future__ import print_function    # (at top of module)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from texttable import Texttable



import json

import time
import sys


auth = oauth2.SpotifyClientCredentials(
    client_id='2af2fa2dd9c147f886a7b67c3d4ca031',
    client_secret='562e93edd67b40cca215c3c882dc41a2'
)

token = auth.get_access_token()
sp = spotipy.Spotify(auth=token)






# returns a list of the names of playlists created by this user
def get_playlist_names(username):


    playlists = sp.user_playlists(username)
    playlist_names = []

    for playlist in playlists['items']:

        # we only want to show playlists created by this user
        # i.e. not other users playlists they have saved to their profile
        if (playlist['owner']['id'] == username):
            playlist_names.append(playlist['name'])

    # test print, TODO Lewis: remove
    #for name in playlist_names:
        #print(name)


    return playlist_names
