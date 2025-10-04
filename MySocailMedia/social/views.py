from django.shortcuts import render
from django.http import HttpResponse
def profile(request):
    return HttpResponse("Hello, world. You're at the profile page.")