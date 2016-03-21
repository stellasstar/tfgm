from django.conf.urls import patterns, include, url
from django.contrib import admin
from waypoints.views import *

urlpatterns = [
            # index page
            url(r'^$', 'gatekeeper.views.index'),           
    
            # Login / logout.
            url(r'^logged_in/$', 'gatekeeper.views.logged_in'),
          
            # using default django auth views with custom templates
            url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
            url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
            
            # Uncomment the next line to enable the admin:       
            url(r'^admin/', include(admin.site.urls)),
            
            # Uncomment the admin/doc line below to enable admin documentation:
            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),            
              
]
