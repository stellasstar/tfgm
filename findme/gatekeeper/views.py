from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from django.contrib.gis import geos

import simplejson

# image processing
from PIL import Image

from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, RedirectView, UpdateView
from gatekeeper import forms, utils
from transport.models import Position
from transport import mapUtils

from django.contrib.auth import authenticate, login, logout

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


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
#                passed = utils.make_thumbnail(pil_image, domain, path)
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

    def form_invalid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)        
        if user is None:
            print "Invalid login details were provided"
            print "We can't log the user in"
            msg = 'Invalid login details supplied.'
            messages.add_message(self.request, messages.ERROR, msg)
        elif not user.is_active:
            msg = 'Your account is disabled.'
            messages.add_message(self.request, messages.ERROR, msg)
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(LoginRequiredMixin, RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        msg = "You are logged out."
        messages.success(self.request, msg)
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
    map_to_show = 'defaultPositionMap'
    GOOGLE_KEY = settings.GOOGLE_API_KEY
    
    def get_object(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        try:
            url = user.picture.url
        except ValueError:
            p = settings.AVATAR_URL.strip('/') + '/' + settings.DEFAULT_AVATAR
            user.picture = p
            user.save()
        return user  # or request.POST    

    def get_context_data(self, **kwargs):
        """
        Load up the default data to
        show in the display form.
        """
        context = super(UserProfileView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        position = self.kwargs.get('position')
        data = {}

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

        # geometry is a gis object.  need to pop out for easier import
        # into data
        position_dict = position.values()[0]
        geometry = position_dict.pop('geometry')

        # get address for location
        if position_dict['address'] is None:
            (address, city) = mapUtils.get_address_from_latlng(geometry.y,
                                                               geometry.x)
            position_dict['address'] = address
            position_dict['city'] = city

        # need to fix this, but if there is an addresss but no coordinate info
        if ((geometry is None) or(geometry.x is None) or (geometry.y is None)):
            try:
                (lat, lng) = mapUtils.get_latlng_from_address(address)
                point = "POINT(%s %s)" % (str(lng), str(lat))
                geometry = geos.fromstr(point)
            except:
                point = "POINT(%s %s)" % (str(settings.DEFAULT_LONGITUDE),
                                          str(settings.DEFAULT_LATITUDE))
                geometry = geos.fromstr(point)

        # update data with user positional data
        data.update(position_dict)
        data['latitude'] = geometry.y
        data['longitude'] = geometry.x
        data['srid'] = geometry.srid

        context['address'] = str(position_dict['address']).split(',')

        # where you want the map to be
        data['map'] = self.map_to_show
        data['GOOGLE_KEY'] = self.GOOGLE_KEY
        context['map'] = self.map_to_show

        cls = simplejson.JSONEncoderForHTML
        context['json_data'] = simplejson.dumps(data, cls=cls)
        context['form'] = form

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
        user = User.objects.get(pk=self.kwargs.get('pk'))
        try:
            url = user.picture.url
        except ValueError:
            p = settings.AVATAR_URL.strip('/') + '/' + settings.DEFAULT_AVATAR
            user.picture = p
            user.save()
        return user  # or request.POST
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        position = Position.objects.filter(user=user)
        last = position.last()
        (address, city) = mapUtils.get_address_from_latlng(last.geometry.y, last.geometry.x)
        context['address'] = str(address).split(',')
        return context
        