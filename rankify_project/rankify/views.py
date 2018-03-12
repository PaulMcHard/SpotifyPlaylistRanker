
from django import forms
from rankify.forms import PlaylistForm
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
from django.contrib.auth import logout as django_logout

from rankify.spotify_utils import get_playlist_names, get_tracks, get_playlists_by_username, get_display_name, get_profile_picture

from rankify.forms import UserForm

from rankify.models import Playlist

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.urls import reverse

# loads of variables to allow the user to authorise this app with their spotify
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
    "client_id": CLIENT_ID,
    "show_dialog": 'true'
}
auth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope = SCOPE )
sp = None
token = None




@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect(reverse('index'))







def index(request):

    # pass a variable to the template to indicate loggined in or not
    logged_in = False
    display_name = ""
    if request.user.is_authenticated: # if active user
        logged_in = True
        display_name = get_display_name(request.user.username)


    return render(request, 'rankify/home.html' , {'logged_in': logged_in, 'display_name': display_name} )


def rankings(request):
    playlist_list = Playlist.objects.order_by('-avg_danceability')[:10]
    creators = []
    for playlist in playlist_list:
        creators.append(get_display_name(playlist.creator.username))



    context_dict = {'playlists': playlist_list, 'display_names': creators}
    return render(request, 'rankify/rankings.html', context_dict)

def user(request):
    #TODO- change this creator to be the user specificed by the url
    #as it stands this shows the active users playlists no matter what profile we are on
    playlist_list = Playlist.objects.filter(creator = request.user)
    users_playlist_list = Playlist.objects.order_by('-avg_danceability')[:5]
    image = get_profile_picture(request.user.username)
    context_dict = {'playlists': playlist_list, 'image_url': image}
    return render(request, 'rankify/user.html', context_dict)




# this is the business function here, adding and processing a playlist to the db
# TODO - this runs slow! can we speed it up somehow?
def add_playlist(request):

    current_user = request.user # get the current users UserProfile
    spotify_username = request.user.username#get their spotify username

    playlists = get_playlists_by_username(spotify_username) #grab their playlists


    CHOICES = [] # create a list of playlist names to pass to the form

    for playlist in playlists['items']:
        already_added = False

        for u_playlist in Playlist.objects.all():
            if playlist['uri'] == u_playlist.spotify_playlist_uri:
                already_added = True


        if already_added == False:
            CHOICES.append((playlist['name'], playlist['name']))

    # create the form, default 'creator' to be the current UserProfile
    form = PlaylistForm(request.POST or None, initial={'creator': current_user,  })
    form.fields['creator'].widget = forms.HiddenInput() #hide this so it cant change

    # set the Playlist 'name' form field to be a dropdown of the above choices
    form.fields['name'] = forms.CharField(max_length=128, label='Select Your Playlist',
    widget=forms.Select(choices=CHOICES))

    if request.method == 'POST': #if we're posting
        if form.is_valid(): #check valid
            added_playlist = form.save(commit=True) #make a new playlist from the form



            playlists = get_playlists_by_username(spotify_username)

            #search this users playlists till we find which one was selected
            for playlist in playlists['items']:
                if playlist['name'] == added_playlist.name:


                    total_danceability = 0
                    track_counter = 0

                    #the get_tracks function does a lot...
                    #it gets tracks from the playlist and adds them to the db as Songs
                    # and returns a list of songs
                    songs = get_tracks(playlist, spotify_username)

                    #add every song in the list to the playlist entry in the db
                    for song in songs:
                        added_playlist.songs.add(song)
                        total_danceability += song.danceability
                        track_counter += 1

                    # add the playlists uri to the db
                    added_playlist.spotify_playlist_uri = playlist['uri']
                    #add the playlists danceability!
                    avg_danceability = total_danceability / track_counter
                    added_playlist.avg_danceability = avg_danceability
                    avg_danceability = round(  avg_danceability, 2 )


                    added_playlist.creator = request.user

                    added_playlist.save() #and save the playlist
                    playlist_added = True
            return render(request, 'rankify/home.html', {'avg_danceability': avg_danceability, 'playlist_added': playlist_added, 'playlist_name': added_playlist.name} )

        else:
            print(form.errors)
            print('INVALID')

    return render(request, 'rankify/add_playlist.html', {'form': form})
