from django.conf.urls import patterns, include, url
from gatekeeper import views

#import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^login/$', views.AccountLogin.as_view(), name="login"),
    url(r'^logout/$', views.AccountLogout.as_view(), name="logout"),
    url(r'^register/$', views.UserRegistrationView.as_view(), name="register"),
]