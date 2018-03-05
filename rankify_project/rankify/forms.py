from django import forms
from django.contrib.auth.models import User
from rankify.models import Playlist, Song, UserProfile

from rankify.spotify_utils import get_playlist_names
from django.contrib import admin


class PlaylistForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        global username
        current_user = kwargs.pop('current_user', None)

        super(PlaylistForm, self).__init__(*args, **kwargs)



    #creator = forms.ModelChoiceField(widget=forms.HiddenInput(), initial = current_user)

    




    avg_danceability = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

    #creator can't be null, so need this line
    #creator = forms.ModelMultipleChoiceField('lewisrenfrew')

    #spotifyPlaylistURI = forms.CharField(widget=forms.HiddenInput(), widget=forms.HiddenInput(),)


    class Meta:
        model = Playlist
        fields = ('name', 'avg_danceability', 'creator')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
