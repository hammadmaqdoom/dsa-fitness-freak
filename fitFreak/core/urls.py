from django.urls import path, include
from . import views

# SET THE NAMESPACE!
# app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    path('loginn', views.loginn, name='loginn'),
    path('logout', views.log_out, name='log_out'),

    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('food', views.food, name='food'),
    path('exercise', views.exercise, name='exercise'),


    path('select_food/', views.select_food, name='select_food'),
    path('add_food/', views.add_food, name='add_food'),
    path('update_food/<str:pk>/', views.update_food, name='update_food'),
    path('delete_food/<str:pk>/', views.delete_food, name='delete_food'),
    path('profile/', views.ProfilePage ,name='profile'),
]