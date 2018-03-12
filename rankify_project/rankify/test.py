import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


auth = oauth2.SpotifyClientCredentials(
    client_id='2af2fa2dd9c147f886a7b67c3d4ca031',
    client_secret='562e93edd67b40cca215c3c882dc41a2'
)

token = auth.get_access_token()
sp = spotipy.Spotify(auth=token)




def get_display_name(username):
    print('ok...')
    user = sp.user_name('werfner')
    print(user)
    return user



get_display_name('werfner')
