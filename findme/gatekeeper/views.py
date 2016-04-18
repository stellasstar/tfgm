from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (Http404, JsonResponse,
                         HttpResponse, HttpResponseNotFound)
from django.contrib import messages
from django.conf import settings
from django.forms.models import model_to_dict

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# image processing
from PIL import Image
import StringIO
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

import os
import simplejson
import json

from django.core.files.base import ContentFile
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, RedirectView, UpdateView
from django.views.generic.edit import ModelFormMixin
from gatekeeper import forms, utils, models
from transport.models import Position

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
        sett = (settings.AVATAR_DEFAULT_HEIGHT, settings.AVATAR_DEFAULT_WIDTH)
        image.thumbnail(sett)
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
                    error = 'File was not a valid image (jpg, jpeg, png, gif)'
                    form.non_field_errors(error)

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

        form.save(commit=True)

        # automatically login after registering
        msg = "Thanks for registering. You are now logged in."
        messages.info(self.request, msg)
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
    redirect_field_name = 'redirect_to'

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


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Profile View Page
    url: profiles/profile_view.html
    """
    template_name = 'profiles/profile_view.html'
    form_class = forms.UserProfileForm
    success_url = "/profiles/"
    model = User
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        """
        Load up the default data to
        show in the display form.
        """
        context = super(UserProfileView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        position = self.kwargs.get('position')
        data = []

        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
            # Case where user gets to this view
            # anonymously for non-existent user

        if user.is_authenticated():
            position = Position.objects.filter(user=user)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return_to = self.request.GET.get('returnTo', '/')
        form = forms.UserProfileForm(instance=user)
        form.initial['returnTo'] = return_to

        position_dict = position.values()[0]
        geometry = position_dict.pop('geometry')

        for key in position_dict.keys():
            value = position_dict.get(key)
            data.append({key: value})

        data.append({'latitude': geometry.y})
        data.append({'longitude': geometry.x})
        data.append({'srid': geometry.srid})

        # where you want the map to be
        data.append({'map': 'defaultPositionMap'})

        cls = simplejson.JSONEncoderForHTML
        context['json_data'] = simplejson.dumps(data, cls=cls)
        context['form'] = form
        context['map'] = 'defaultPositionMap'

        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = forms.UserProfileUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = "/update/"
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        return reverse('update', kwargs={
            'pk': self.kwargs.get('pk')})

    def get_object(self):
        return User.objects.get(pk=self.kwargs.get('pk'))  # or request.POST
