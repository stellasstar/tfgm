from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpResponse

from django.views.generic.edit import BaseCreateView, FormView
from django.views.generic import CreateView, RedirectView
from gatekeeper.forms import UserRegistrationForm, LoginForm
from django.contrib import messages 

from django.contrib.auth import authenticate, login, logout

#import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'registration/register.html'
    success_url = '/'

    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(self.request, self.template_name, {'form':form})
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form':form})
        #return super(UserRegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        password = form.cleaned_data['password']
        self.object.set_password(password)
        self.object.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/activate.html',
            'subject_template_name': 'registration/activation_email_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
# NEED TO FIX THIS
        reset_form.save(**opts)

	return redirect(self.success_url)

class LoginView(FormView):
    
    form_class = LoginForm
    success_url = '/'
    template_name = 'registration/login.html'
    model = User
    
    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(self.request, self.template_name, {'form':form})
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form':form})    

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