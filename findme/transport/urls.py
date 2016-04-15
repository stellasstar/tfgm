from django.conf.urls import include, url

from django.contrib import admin
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from transport.views import WaypointView


admin.autodiscover()

urlpatterns = [
    
        # Transportation
        url(r'^nearby/$',
            TemplateView.as_view(template_name='transport/nearby.html'),
            name='near-me'),   
              
        url(r'^$', WaypointView.as_view(), name='transport'), 

]