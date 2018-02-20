from django.shortcuts import render
from django.http import HttpResponse




def index(request):
    return render(request, 'rankify/home.html')


def rankings(request):
    return render(request, 'rankify/rankings.html')

def user(request):
    return render(request, 'rankify/user.html')
