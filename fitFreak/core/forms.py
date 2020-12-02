# core/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Food,Profile


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Enter email', widget=forms.TextInput(attrs={'placeholder': 'abcd@gmail.com'}))
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

# class CustomLoginForm(forms.Form):
#     username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
#     password = forms.CharField(label='Enter password', widget=forms.PasswordInput)

#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         r = User.objects.filter(username=username)
#         if not r.count():
#             raise  ValidationError("Username does not exist")
#         return username
    
#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         return password

class SelectFoodForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('food_selected','quantity',)

    def __init__(self, user, *args, **kwargs):
        super(SelectFoodForm, self).__init__(*args, **kwargs)
        self.fields['food_selected'].queryset = Food.objects.filter(person_of=user)

class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name','quantity','calorie')

   
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('calorie_goal',)