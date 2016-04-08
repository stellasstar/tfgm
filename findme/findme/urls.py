from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views
from findme.views import HomePageView, ContactFormView
from django.conf import settings
from django.views.static import * 

admin.autodiscover()

urlpatterns = [
            # index page
            url(r'^$', HomePageView.as_view(), name='home'), 
            url(r'^contact/$', ContactFormView.as_view(), name='contact'),
            url(r'^gatekeeper/', include('gatekeeper.urls')),
            url(r'^transport/', include('transport.urls')),            
            
            # Uncomment the next line to enable the admin:       
            url(r'^admin/', include(admin.site.urls)),
            
            # Uncomment the admin/doc line below to enable admin documentation:
            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),  
            
            # media and static files
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT}, name="media"),
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
                }),            
              
]
