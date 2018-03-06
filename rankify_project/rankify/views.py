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
    "client_id": CLIENT_ID,
    "show_dialog": 'true'
}
auth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope = SCOPE )
sp = None
token = None


def user_login(request):
    # djangos machinery handles this, pretty much a straight life from TWD book
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user: #if we got a user

            if user.is_active:#and they are active
                #django login
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    else:     # This scenario would most likely be a HTTP GET.
        # blank dictionary object... nothing to pass back
        return render(request, 'rankify/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))


def link_spotify(request):
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,urlquote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    #return HttpResponse(auth_url)
    return HttpResponseRedirect(auth_url,)

# step 2, call back, if this function executes succesfully then a spotify account
# (username and uri) will be linked to the active django users UserProfile object
def callback(request):

    token_code = request.GET.get('code')
    if(token_code): #if we got a code
        token = auth.get_access_token(token_code) #get a token
        sp = spotipy.Spotify(auth=token['access_token']) #can use spotipy now
        user = sp.me() # get the user
        username = user['id'] #thier spotify username
        uri = user['uri'] #their spotify uri
        playlists = sp.user_playlists(user['id']) #a list of their playlists

        u = UserProfile.objects.get(user = request.user)  #get the current UserProgile
        u.spotify_user_uri = user['uri']  # assign it this spotify uri
        u.spotify_username = username # assign it this spotify username



        u.save() # save the changes to the active users UserProfile
        if (u.spotify_user_uri): #if they active user has a linked spotify account
            spotify_linked = True # set this true so we can pass it to the template
        return render(request, 'rankify/home.html', {'spotify_linked': spotify_linked,})

    else: # if we dont have a code this time
        # return to the home page,
        return HttpResponseRedirect(reverse('index'), )

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
    spotify_linked = False #track whether the user has a linked spotify account

    if request.user.is_authenticated: # if active user
        u = UserProfile.objects.get(user = request.user) #get associated UserProfile
        if (u.spotify_user_uri): # if they have a spotify uri associated with UserProfile
            spotify_linked = True #they must have linked their spotify
    # pass spotify_linked (T or F) to the template long with the request
    return render(request, 'rankify/home.html' , {'spotify_linked': spotify_linked,} )


def rankings(request):
    return render(request, 'rankify/rankings.html')

def user(request):
    return render(request, 'rankify/user.html')


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                # Now we save the UserProfile model instance.
                profile.save()
                # Update our variable to indicate that the template
                # registration was successful.
                registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'rankify/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

# this is the business function here, adding and processing a playlist to the db
# TODO - this runs slow! can we speed it up somehow?
def add_playlist(request):
    current_user = UserProfile.objects.get(user=request.user) # get the current users UserProfile
    spotify_username = current_user.spotify_username #get their spotify username


    playlists = get_playlists_by_username(spotify_username) #grab their playlists
    CHOICES= [] # create a list of playlist names to pass to the form
    for s_playlist in playlists['items']:
        already_added = False
        for playlist in Playlist.objects.all():
            if s_playlist['uri'] == playlist.spotify_playlist_uri:
                already_added = True


        if already_added == False:
            CHOICES.append((s_playlist['name'], s_playlist['name']))

    # create the form, default 'creator' to be the current UserProfile
    form = PlaylistForm(request.POST or None, initial={'creator': current_user,  })
    form.fields['creator'].widget = forms.HiddenInput() #hide this so it cant change

    # set the Playlist 'name' form field to be a dropdown of the above choices
    form.fields['name'] = forms.CharField(max_length=128, label='Select Your Playlist',
    widget=forms.Select(choices=CHOICES))

    if request.method == 'POST': #if we're posting
        if form.is_valid(): #check valid
            added_playlist = form.save(commit=True) #make a new playlist from the form


            # get playlists by username
            user_profile = UserProfile.objects.get(user =request.user)
            username = user_profile.spotify_username
            playlists = get_playlists_by_username(username)

            #search this users playlists till we find which one was selected
            for playlist in playlists['items']:
                if playlist['name'] == added_playlist.name:


                    total_danceability = 0
                    track_counter = 0

                    #the get_tracks function does a lot...
                    #it gets tracks from the playlist and adds them to the db as Songs
                    # and returns a list of songs
                    songs = get_tracks(playlist, username)

                    #add every song in the list to the playlist entry in the db
                    for song in songs:
                        added_playlist.songs.add(song)
                        total_danceability += song.danceability
                        track_counter += 1

                    # add the playlists uri to the db
                    added_playlist.spotify_playlist_uri = playlist['uri']
                    #add the playlists danceability!
                    added_playlist.avg_danceability = total_danceability / track_counter

                    added_playlist.save() #and save the playlist
            return HttpResponseRedirect(reverse('index'))

        else:
            print(form.errors)
            print('INVALID')

    return render(request, 'rankify/add_playlist.html', {'form': form})
