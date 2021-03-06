from django import forms
from rankify.forms import PlaylistForm
import sys
import math
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
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from rankify.spotify_utils import  get_tracks, get_playlists_by_username, get_display_name, get_profile_picture
from rankify.forms import UserForm
from rankify.models import Playlist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render

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
    for playlist in session['playlists']:
        playlist.avg_danceability = round(playlist.avg_danceability, 2)


    return render(request, 'rankify/rankings.html', session)



def user(request):
    context_dict = getSession(request)
    try:
        user = request.user
        username = user.username
        playlist_list = Playlist.objects.filter(creator = request.user)
        playlist_list = playlist_list.order_by('-avg_danceability')[:5]
        image = get_profile_picture(request.user.username)






        context_dict['playlists'] = playlist_list
        for playlist in context_dict['playlists']:
            playlist.avg_danceability = round(playlist.avg_danceability, 2)
        context_dict['user'] = user
        context_dict['username'] = username
        if image == 'no picture set!!':
            context_dict['image_url'] = "static/img/default_avatar.jpg"
            print(context_dict['image_url'])
        else:
            context_dict['image_url'] = image
            print(context_dict['image_url'])


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
        if not get_display_name(request.user.username):
            session['display_name'] = request.user.username

        else:
            session['display_name'] = get_display_name(request.user.username)

    if request.GET.get("ajax") == "true":
        session['ajaxProofTemplate'] = 'rankify/ajaxbase.html'
    else:
        session['ajaxProofTemplate'] = 'rankify/base.html'

    return session



# this is the business function here, adding and processing a playlist to the db
@login_required
def add_playlist(request):

    session = getSession(request)

    current_user = request.user # get the current users
    spotify_username = request.user.username #get their spotify username

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

                    total_score = 0
                    total_danceability = 0
                    track_counter = 0

                    #the get_tracks function does a lot...
                    #it gets tracks from the playlist and adds them to the db as Songs
                    # and returns a list of songs
                    songs = get_tracks(playlist, spotify_username)

                    #add every song in the list to the playlist entry in the db
                    for song in songs:
                        added_playlist.songs.add(song)
                        score = ( song.danceability * 100)
                        score = round(score, 2)
                        total_danceability += song.danceability
                        total_score += score
                        track_counter += 1

                    # add the playlists uri to the db
                    added_playlist.spotify_playlist_uri = playlist['uri']
                    #add the playlists danceability!
                    avg_score = 0
                    avg_danceability = 0

                    if track_counter > 0:
                        avg_danceability = total_danceability / track_counter
                        avg_danceability = round(avg_danceability, 2)
                        avg_score = total_score / track_counter
                        avg_score = round(avg_score, 2)
                    added_playlist.avg_danceability = avg_danceability
                    added_playlist.total_danceability = total_danceability

                    added_playlist.creator = request.user
                    added_playlist.playlist_image_url = get_profile_picture(request.user.username)
                    display_name = get_display_name(request.user.username)

                    #not all spotify users have a display name, use their username if this is the case
                    if display_name:
                        added_playlist.creator_display_name = display_name
                    else:
                        added_playlist.creator_display_name = request.user.username

                    added_playlist.save() #and save the playlist
                    playlist_added = True

            session['avg_danceability'] = avg_danceability
            session['total_danceability'] = int(total_danceability)
            session['avg_score'] = avg_score
            session['total_score'] = int(total_score)
            session['playlist_added'] = playlist_added
            session['playlist_name'] = added_playlist.name
            session['number'] = 4
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

    #get av danceability and set variance and counter.
    mean = (playlist.avg_danceability * 100)

    variance = 0
    count = 0

    #for each song get variance from mean and use that to calculate standard Deviation
    for song in songs:
        score = ( song.danceability * 100 )
        score = round(score, 2)
        thisvar = score - mean
        thisvar = thisvar ** 2
        variance += thisvar
        count += 1
        song.score = score

    if count > 0:
        meanvar = variance/count
    else: #avoid divide by zero problem
        meanvar = 0;

    stdDev = math.sqrt(meanvar)
    stdDev = (round(stdDev, 3))
    mean = (round(mean, 3))

    abovedev = []
    belowdev = []

    for song in songs:
        if( ( song.score ) > ( mean + stdDev )):
            abovedev.append(song)
        elif ( ( song.score ) < ( mean - stdDev )):
            belowdev.append(song)

    #abovedev = sort(key = lambda danceability: song.danceability )
    #belowdev.sort(key = lambda danceability: song.danceability )

    abovedev = sorted(abovedev, key = lambda danceability:  song.score )

    context_dict['deviation'] =stdDev
    context_dict['mean'] = mean
    context_dict['abovedev'] = abovedev
    context_dict['belowdev'] = belowdev
    context_dict['avg_danceability'] = playlist.avg_danceability

    return render(request, 'rankify/playlist.html', context_dict)

def remove_playlist(request, playlist_slug):
    context_dict = getSession(request)

    removeList = Playlist.objects.get(slug=playlist_slug)
    playlists = Playlist.objects.filter(creator = request.user)
    for playlist in playlists:
        if playlist.SlugField == removeList:
            playlists.remove(playlist)

    return render(request, 'rankify/user.html', context_dict)
