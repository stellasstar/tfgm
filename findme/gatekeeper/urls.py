from django.conf.urls import url
from django.contrib.auth import views
from gatekeeper.views import (UserRegistrationView, LoginView, LogOutView,
                              UserProfileView, UserProfileUpdateView)

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    # Login/Logout
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),

    # Profiles
    url(r'^profiles/$', UserProfileView.as_view(), name='profile_view'),
    url(r'^update/(?P<pk>\d+)/$', UserProfileUpdateView.as_view(),
        name='update'),

    # Registration
    url(r'^register/$', UserRegistrationView.as_view(), name="register"),
    url(r'^register/done/$', views.password_reset_done, {
        'template_name': 'registration/initial_done.html',
    }, name='register-done'),
    url(r'^register/complete/$', views.password_reset_complete, {
        'template_name': 'registration/initial_complete.html',
    }, name='register-complete'),

]
