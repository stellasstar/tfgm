from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views
from gatekeeper.views import HomePageView

admin.autodiscover()

urlpatterns = [
            # index page
            # index page
            url(r'^$', HomePageView.as_view(), name='home'), 
            url(r'^gatekeeper/', include('gatekeeper.urls')),
            
            # Uncomment the next line to enable the admin:       
            url(r'^admin/', include(admin.site.urls)),
            
            # Uncomment the admin/doc line below to enable admin documentation:
            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),            
              
]
