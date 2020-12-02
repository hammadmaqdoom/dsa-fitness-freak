from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SelectFoodForm, AddFoodForm, CustomUserCreationForm, ProfileForm
from .models import *
from datetime import timedelta
from django.utils import timezone
from datetime import date
from datetime import datetime
from django.http import HttpResponseRedirect
from .filters import FoodFilter


def index(request):
    return render(request,"index.html", {'type': 'index-page'})

def home(request):
    return render(request,"home.html", {'type': 'index-page'})

def about(request):
    return render(request,"about.html", {'type': 'index-page'})

def loginn(request):
    if request.method == "POST":
        f = AuthenticationForm(request, data=request.POST)
        if f.is_valid():
            username = f.cleaned_data.get('username')
            password = f.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    f = AuthenticationForm()
    return render(request,"login.html", {'type': 'register-page', 'form': f })

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

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
    if not request.user.is_authenticated:
        return render(request,"login.html", {'type': 'register-page'})
    else:
        #taking the latest profile object
        calories = Profile.objects.filter(person_of=request.user).last()
        calorie_goal = calories.calorie_goal
        
        #creating one profile each day
        if date.today() > calories.date:
            profile=Profile.objects.create(person_of=request.user)
            profile.save()
        calories = Profile.objects.filter(person_of=request.user).last()
        # showing all food consumed present day

        all_food_today=PostFood.objects.filter(profile=calories)
        
        calorie_goal_status = calorie_goal -calories.total_calorie
        over_calorie = 0
        if calorie_goal_status < 0 :
            over_calorie = abs(calorie_goal_status)

        context = {
        'total_calorie':calories.total_calorie,
        'calorie_goal':calorie_goal,
        'calorie_goal_status':calorie_goal_status,
        'over_calorie' : over_calorie,
        'food_selected_today':all_food_today,
        'type': 'index-page'
        }
        
        return render(request,"food.html", context)

def select_food(request):
	person = Profile.objects.filter(person_of=request.user).last()
	#for showing all food items available
	food_items = Food.objects.filter(person_of=request.user)
	form = SelectFoodForm(request.user,instance=person)

	if request.method == 'POST':
		form = SelectFoodForm(request.user,request.POST,instance=person)
		if form.is_valid():
			
			form.save()
			return redirect('home')
	else:
		form = SelectFoodForm(request.user)

	context = { 'form':form,
                'food_items':food_items,
                'type': 'index-page',
            }
	return render(request, 'select_food.html',context)

#for adding new food
def add_food(request):
	#for showing all food items available
	food_items = Food.objects.filter(person_of=request.user)
	form = AddFoodForm(request.POST) 
	if request.method == 'POST':
		form = AddFoodForm(request.POST)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.person_of = request.user
			profile.save()
			return redirect('add_food')
	else:
		form = AddFoodForm()
		
	#for filtering food
	myFilter = FoodFilter(request.GET,queryset=food_items)
	food_items = myFilter.qs
	context = {'form':form,'food_items':food_items,'myFilter':myFilter,'type': 'index-page'}
	return render(request,'add_food.html',context)

#for updating food given by the user
@login_required
def update_food(request,pk):
	food_items = Food.objects.filter(person_of=request.user)

	food_item = Food.objects.get(id=pk)
	form =  AddFoodForm(instance=food_item)
	if request.method == 'POST':
		form = AddFoodForm(request.POST,instance=food_item)
		if form.is_valid():
			form.save()
			return redirect('profile')
	myFilter = FoodFilter(request.GET,queryset=food_items)
	context = {'form':form,'food_items':food_items,'myFilter':myFilter,'type': 'index-page'}

	return render(request,'add_food.html',context)

#for deleting food given by the user
@login_required
def delete_food(request,pk):
	food_item = Food.objects.get(id=pk)
	if request.method == "POST":
		food_item.delete()
		return redirect('profile')
	context = {'food':food_item,'type': 'index-page'}
	return render(request,'delete_food.html',context)

#profile page of user
@login_required
def ProfilePage(request):
	#getting the lastest profile object for the user
	person = Profile.objects.filter(person_of=request.user).last()
	food_items = Food.objects.filter(person_of=request.user)
	form = ProfileForm(instance=person)

	if request.method == 'POST':
		form = ProfileForm(request.POST,instance=person)
		if form.is_valid():	
			form.save()
			return redirect('profile')
	else:
		form = ProfileForm(instance=person)

	#querying all records for the last seven days 
	some_day_last_week = timezone.now().date() -timedelta(days=7)
	records=Profile.objects.filter(date__gte=some_day_last_week,date__lt=timezone.now().date(),person_of=request.user)

	context = {'form':form,'food_items':food_items,'records':records,'type': 'index-page',}
	return render(request, 'profile.html',context)

def exercise(request):
    if not request.user.is_authenticated:
        return render(request,"login.html", {'type': 'register-page'})
    else:
        return render(request,"exercise.html", {'type': 'index-page'})

def contact(request):
    return render(request,"contact.html", {'type': 'profile-page'})
