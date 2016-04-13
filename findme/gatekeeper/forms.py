
# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.gis.geos import Point, GEOSException, GEOSGeometry, fromstr
from django.conf import settings
from django.forms.models import inlineformset_factory

from imagekit.models import ProcessedImageField

from transport.models import Position

import httplib

class LoginForm(AuthenticationForm):

        username = forms.CharField(required=True)
        password = forms.CharField(widget=forms.PasswordInput)

        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.add_input(Submit('submit',
                                         'Submit',
                                         css_class='btn-primary'))
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
                
      #  widgets = {'thumbnail': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                    'Register',
                                     css_class='btn-primary'))
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True, *args, **kwargs):
        lString = 'POINT(%s %s)' % (str(self.fields['longitude'].initial), str(self.fields['latitude'].initial))
        picture = self.fields['picture']
        new_user = super(UserRegistrationForm, self).save(commit=False, *args, **kwargs)
        new_position = Position(
            user = new_user,
            name=self.cleaned_data['username'],
            geometry = fromstr(lString))       
        if commit:
            new_user.save()
            new_position.save()
            new_user.position = new_position            
            new_user.save()          
        return new_user, new_position 

class UserProfileForm(forms.ModelForm):
    """Form for editing the data that is part of the User model"""

    class Meta():
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'homepage',
                  'picture',
                  'latitude',
                  'longitude',
                  ]  

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)


class UserProfileUpdateForm(forms.ModelForm):
    """Form for editing the data that is part of the User model"""

    class Meta():
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'homepage',
                  'picture',
                  'latitude',
                  'longitude',
                  ]  

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                     'Update',
                                     css_class='btn-primary'))   
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

    def save(self, user=None):
        user_profile = super(UserProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile    
    
    
    
