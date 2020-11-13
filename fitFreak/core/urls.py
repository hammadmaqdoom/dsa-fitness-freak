from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('about', views.about, name='about'),
    path('signup', views.signup, name='signup'),
    path('contact', views.contact, name='contact'),
    path('food', views.food, name='food'),
    path('exercise', views.exercise, name='exercise'),
]