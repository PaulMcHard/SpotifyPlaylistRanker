

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



from rankify.forms import UserForm, UserProfileForm
from rankify.models import UserProfile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse


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


def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
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
    return HttpResponseRedirect(auth_url)


def callback(request):
    token_code = request.GET.get('code')
    token = auth.get_access_token(token_code)
    sp = spotipy.Spotify(auth=token['access_token'])
    user = sp.me()
    username = user['display_name']
    uri = user['uri']
    print(uri)
    playlists = sp.user_playlists(user['id'])
    loggedIn = True

    current_user = request.user
    username = current_user.username


    user_profiles = UserProfile.objects.filter(user = request.user)
    for u in user_profiles:


        u.spotifyUserURI = user['uri']  # change field
        u.save()


    return render(request, 'rankify/home.html', {'loggedIn': loggedIn, 'username': username})
    #return HttpResponseRedirect(reverse('index'), )


def index(request):
    return render(request, 'rankify/home.html')


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


def add_playlist(request):
    form = PlaylistForm(request.POST)

    if form.is_valid():
        playlist = form.save(commit=True)

        playlist.save()
        return index(request)
    else:
        print(form.errors)
        print('INVALID')

    return render(request, 'rankify/add_playlist.html', {'form': form})
