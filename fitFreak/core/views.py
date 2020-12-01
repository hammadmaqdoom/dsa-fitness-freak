from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from datetime import date
from datetime import datetime


def index(request):
    return render(request,"index.html", {'type': 'index-page'})

def about(request):
    return render(request,"about.html", {'type': 'index-page'})

def loginn(request):
    return render(request,"login.html", {'type': 'register-page'})

def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect("signup")

    else:
        f = CustomUserCreationForm()
        return render(request,"signup.html", {'type': 'register-page', 'form': f })

def food(request):
    return render(request,"food.html", {'type': 'index-page'})

def exercise(request):
    return render(request,"exercise.html", {'type': 'index-page'})

def contact(request):
    return render(request,"contact.html", {'type': 'profile-page'})
