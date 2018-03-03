from django import forms
from django.contrib.auth.models import User
from rankify.models import Playlist, Song, UserProfile

from rankify.spotify_utils import get_playlist_names
from django.contrib import admin


class PlaylistForm(forms.ModelForm):

    creator = forms.ModelChoiceField(queryset=UserProfile.objects.all())

    PLAYLISTS = get_playlist_names('alicejanehughes')



    CHOICES= []
    counter = 0
    for playlist in PLAYLISTS:
        CHOICES.append((counter, playlist))

    creator = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    #name = forms.CharField(max_length=128, label='Select Your Playlist',
    #widget=forms.Select(choices=CHOICES))

    #creator can't be null, so need this line
    #creator = forms.ModelMultipleChoiceField('lewisrenfrew')

    #spotifyPlaylistURI = forms.CharField(widget=forms.HiddenInput(), initial = " ")


    class Meta:
        model = Playlist
        fields = ('spotifyPlaylistURI', 'name', 'avgDanceability', 'songs', 'creator')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
