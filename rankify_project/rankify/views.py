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
from django.contrib.auth.models import User
from rankify.spotify_utils import  get_tracks, get_playlists_by_username, get_display_name, get_profile_picture
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
    return render(request, 'rankify/home.html' , getSession(request) )



def rankings(request):
    playlist_list = Playlist.objects.order_by('-avg_danceability')[:10]
    session = getSession(request)
    session['playlists'] = playlist_list
    return render(request, 'rankify/rankings.html', session)



def user(request):
    #TODO- change this creator to be the user specificed by the url
    #as it stands this shows the active users playlists no matter what profile we are on
    context_dict = getSession(request)
    try:
        user = request.user
        username = user.username
        playlist_list = Playlist.objects.filter(creator = request.user)
        playlist_list = playlist_list.order_by('-avg_danceability')[:5]
        image = get_profile_picture(request.user.username)
        context_dict['playlists'] = playlist_list
        context_dict['user'] = user
        context_dict['username'] = username
        context_dict['image_url'] = image

    except User.DoesNotExist:
        context_dict['playlists'] = None
        context_dict['user'] = None
        context_dict['username'] = None
        context_dict['image_url'] = None

    return render(request, 'rankify/user.html', context_dict )



def show_user(request, username):
    context_dict = getSession(request)
    the_user = None

    for user in User.objects.all():
        if user.username == username:
            the_user = user

    playlist_list = Playlist.objects.filter(creator = the_user)
    playlist_list = playlist_list.order_by('-avg_danceability')[:5]
    image = get_profile_picture(username)
    context_dict['playlists'] = playlist_list
    context_dict['username'] = username
    context_dict['image_url'] = image

    return render(request, 'rankify/user.html', context_dict )



def getSession(request):
    session = {}
    # pass a variable to the template to indicate loggined in or not
    session['logged_in'] = False
    session['display_name'] = ""
    if request.user.is_authenticated: # if active user
        session['logged_in'] = True
        session['display_name'] = get_display_name(request.user.username)

    if request.POST.get("ajax") == "true":
        session['ajaxProofTemplate'] = 'rankify/ajaxbase.html'
    else:
        session['ajaxProofTemplate'] = 'rankify/base.html'

    return session



# this is the business function here, adding and processing a playlist to the db
# TODO - this runs slow! can we speed it up somehow?
def add_playlist(request):

    session = getSession(request)

    current_user = request.user # get the current users UserProfile
    spotify_username = request.user.username#get their spotify username

    playlists = get_playlists_by_username(spotify_username) #grab their playlists


    CHOICES = [] # create a list of playlist names to pass to the form

    for playlist in playlists['items']:
        already_added = False

        for u_playlist in Playlist.objects.all():
            if playlist['uri'] == u_playlist.spotify_playlist_uri:
                already_added = True


        if (already_added == False) and (playlist['owner']['id'] == request.user.username):
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
                    avg_danceability = 0
                    if track_counter > 0:
                        avg_danceability = total_danceability / track_counter
                    added_playlist.avg_danceability = avg_danceability
                    avg_danceability = round(  avg_danceability, 2 )


                    added_playlist.creator = request.user
                    print(playlist['images'][0]['url'])
                    added_playlist.playlist_image_url = get_profile_picture(request.user.username)
                    display_name = get_display_name(request.user.username)

                    #not all spotify users have a display name, user their username if this is the case
                    if display_name:
                        added_playlist.creator_display_name = display_name
                    else:
                        added_playlist.creator_display_name = request.user.username

                    added_playlist.save() #and save the playlist
                    playlist_added = True

            session['avg_danceability'] = avg_danceability
            session['playlist_added'] = playlist_added
            session['playlist_name'] = added_playlist.name
            return render(request, 'rankify/home.html', session )

        else:
            print(form.errors)
            print('INVALID')

    session['form'] = form
    return render(request, 'rankify/add_playlist.html', session)



def show_playlist(request, playlist_slug):
    context_dict = getSession(request)

    #check this playlist exists in the db
    playlist = Playlist.objects.get(slug=playlist_slug)

    #get its songs
    songs = playlist.songs.all()

    # stick them in the dictionary
    context_dict['songs'] = songs

    return render(request, 'rankify/playlist.html', context_dict)
