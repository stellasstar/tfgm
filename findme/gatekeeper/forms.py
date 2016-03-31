
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
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Layout
import floppyforms

class LoginForm(AuthenticationForm):
    
        username = floppyforms.CharField(required=True)
        password = forms.CharField(widget=forms.PasswordInput)      
    
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
            super(LoginForm, self).__init__(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):

    required_css_class = 'required'
    
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ['first_name', 
                  'last_name',
                  'username', 
                  'email', 
                  'password', 
                  'password_confirm',
                  'homepage', 
                  'picture', 
                  'latitude', 
                  'longitude',
        ]

     
