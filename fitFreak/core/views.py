from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request,"index.html", {'type': 'index-page'})

def about(request):
    return render(request,"about.html", {'type': 'index-page'})

def login(request):
    return render(request,"login.html", {'type': 'register-page'})

def signup(request):
    return render(request,"signup.html", {'type': 'register-page'})

def food(request):
    return render(request,"food.html", {'type': 'index-page'})

def exercise(request):
    return render(request,"exercise.html", {'type': 'index-page'})

def contact(request):
    return render(request,"contact.html", {'type': 'profile-page'})
    