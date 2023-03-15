from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("You're at store's index page.")
