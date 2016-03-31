from django.conf.urls import patterns, include, url
from gatekeeper.views import UserRegistrationView, LoginView, LogOutView, UserProfileView
from django.contrib.auth import views

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
    
    # Registration
    url(r'^register/$', UserRegistrationView.as_view(), name="register"),
    url(r'^register/done/$', views.password_reset_done, {
        'template_name': 'registration/initial_done.html',
    }, name='register-done'),

    url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, {
        'template_name': 'registration/initial_confirm.html',
        'post_reset_redirect': 'gatekeeper:register-complete',
    }, name='register-confirm'),
    url(r'^register/complete/$', views.password_reset_complete, {
        'template_name': 'registration/initial_complete.html',
    }, name='register-complete'),
    
    # Login/Logout
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    
    # Profiles
    url(r'^profiles/$', UserProfileView.as_view(), name='profile_view'),
]
