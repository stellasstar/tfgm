import re
from gatekeeper.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')  

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('homepage', 'picture', 'latitude', 'longitude')
