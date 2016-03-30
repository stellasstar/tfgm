
#import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
import re

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ['username', 
                  'email', 
                  'password', 
                  'password_confirm'
        ]

     
