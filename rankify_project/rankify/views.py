import sys
import json
import requests
import base64
import urllib
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, redirect, g, render_template

#  Client Keys
CLIENT_ID = "2af2fa2dd9c147f886a7b67c3d4ca031"
CLIENT_SECRET = "562e93edd67b40cca215c3c882dc41a2"
# Spotify URL
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT=8000
REDIRECT_URI = "{}:{}/rankify/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}
auth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope = SCOPE )

def login(request):
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,urlquote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    #return HttpResponse(auth_url)
    return HttpResponseRedirect(auth_url)


def callback(request):
    token_code = request.GET.get('code')
    token = auth.get_access_token(token_code)
    sp = spotipy.Spotify(auth=token['access_token'])
    user = sp.me()
    username = user['display_name']
    playlists = sp.user_playlists(user['id'])
    loggedIn = True
    return render(request, 'rankify/home.html', {'loggedIn': loggedIn, 'username': username})


def index(request):
    return render(request, 'rankify/home.html')


def rankings(request):
    return render(request, 'rankify/rankings.html')

def user(request):
    return render(request, 'rankify/user.html')
