from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# image processing
from PIL import Image
import StringIO
from django.core.files.storage import default_storage

from django.core.files.uploadedfile import InMemoryUploadedFile

import os
import json


from django.core.files.base import ContentFile
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from gatekeeper import forms, utils, models

from django.contrib.auth import authenticate, login, logout

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


def make_thumbnail(image, name, ext):
    """
    Create and save the thumbnail for the photo (simple resize with PIL).
    """
    try:
        image = Image.open(User.thumbnail)
        image.thumbnail((settings.AVATAR_DEFAULT_HEIGHT, settings.AVATAR_DEFAULT_WIDTH))
    except IOError:
        return False
    
    thumb_buffer = StringIO.StringIO()
    
    image.save(thumb_buffer, format=image.format)    
    thumb_name, thumb_extension = (name.lower(), ext.lower())
    thumb = models.Avatar_User_Dir(thumb_name + '_thumb' + thumb_extension)

    s3_thumb = default_storage.open(thumb, 'w')
    s3_thumb.write(thumb_buffer.getvalue())
    s3_thumb.close()   
    
    return True
    

class UserRegistrationView(CreateView):

    form_class = forms.UserRegistrationForm
    model = User
    template_name = 'registration/register.html'
    success_url = '/'

    def get(self, request):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
                          self.get_context_data(form=form))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})
        # return super(UserRegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        self.object, new_position = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        self.object.set_password(password)
        
        url = form.cleaned_data['picture']
            
        if url and not str(url).find('Default'):
            
            domain, path = utils.split_url(str(url))
            
            try:
                extension = utils.valid_url_extension(str.lower(path))
            except not extension:
                    form.non_field_errors('File was not a valid image (jpg, jpeg, png, gif)')  

            try:
                pil_image = Image.open(url)
            except utils.valid_image_size(pil_image):
                form.non_field_errors('Image is too large (> 4mb)')
            
            #  saving this for later
#            try:
#                passed = False
#                passed = make_thumbnail(pil_image, domain, path) 
#            except not passed:
#                form.non_field_errors("Couldn't make thumbnail image")
        

        # save the form
        self.object.save()        
        
        # automatically login after registering 
        messages.info(self.request, "Thanks for registering. You are now logged in.")
        new_user = authenticate(username=username,
                                password=password)
        if new_user is not None and new_user.is_active:
            login(self.request, new_user)
        
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https':
                self.request.is_secure(),
            'email_template_name':
                'registration/activate.html',
            'subject_template_name':
                'registration/activation_email_subject.txt',
            'request': self.request,
            # 'html_email_template_name':
            # provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect(self.success_url)


class LoginView(FormView):

    form_class = forms.LoginForm
    success_url = '/'
    template_name = 'registration/login.html'
    model = User

    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class UserProfileView(TemplateView):
    """
    Profile View Page
    url: profiles/profile_view.html
    """
    template_name = 'profiles/profile_view.html'
    form_class = forms.UserProfileForm

    def get_context_data(self, **kwargs):
        """
        Load up the default data to
        show in the display form.
        """
        username = self.kwargs.get('username')

        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            raise Http404
            # Case where user gets to this view
            # anonymously for non-existent user

        return_to = self.request.GET.get('returnTo', '/')
        form = forms.UserProfileForm(instance=user)
        form.initial['returnTo'] = return_to
        return {'form': form}
        
    
class UserProfileUpdateView(UpdateView):
    
    model = User
    form_class = forms.UserProfileUpdateForm 
    template_name='profiles/profile_update.html'
    success_url = "/update/"
    
    def get_success_url(self):
        return reverse('update', kwargs={
            'pk': self.object.pk,})
    
    def get_object(self):
        return User.objects.get(pk=self.kwargs.get('pk')) # or request.POST  
    
    