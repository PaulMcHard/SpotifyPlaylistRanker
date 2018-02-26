from django.shortcuts import render
from django.http import HttpResponse
from Naked.toolshed.shell import execute_js, muterun_js
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def login(request):
    #muterun_js('templates/authorization_code/app.js')
    return render(request, 'authorization_code/public/index.html')


def index(request):
    return render(request, 'rankify/home.html')


def rankings(request):
    return render(request, 'rankify/rankings.html')

def user(request):
    return render(request, 'rankify/user.html')
