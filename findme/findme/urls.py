from django.conf.urls import patterns, include, url
from django.contrib import admin
from waypoints.views import *
from gatekeeper.views import *

urlpatterns = [
            # index page
            url(r'^$', 'django.contrib.auth.views.login'),
            url(r'^logout/$', logout_page),
            url(r'^accounts/login/$', 'django.contrib.auth.views.login'), 
            # If user is not login it will redirect to login page
            url(r'^register/$', register),
            url(r'^register/success/$', register_success),
            url(r'^home/$', home),
            
            # Uncomment the next line to enable the admin:       
            url(r'^admin/', include(admin.site.urls)),
            
            # Uncomment the admin/doc line below to enable admin documentation:
            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),            
              
]
