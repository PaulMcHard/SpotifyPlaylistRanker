from django import forms
from django.contrib.auth.models import User
from rankify.models import Playlist, Song


from django.contrib import admin


class PlaylistForm(forms.ModelForm):

    avg_danceability = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)


    class Meta:
        model = Playlist
        fields = ('name', 'avg_danceability', 'creator')



# not suer we'll need this now that spotify handles all our auth, but left it for now
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
