from django.urls import path
from . import views

# SET THE NAMESPACE!
# app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('loginn', views.loginn, name='loginn'),
    path('about', views.about, name='about'),
    path('signup', views.signup, name='signup'),
    path('contact', views.contact, name='contact'),
    path('food', views.food, name='food'),
    path('exercise', views.exercise, name='exercise'),
]