from django.conf.urls import url

from django.contrib import admin
from transport.views import WaypointView, AddComments


admin.autodiscover()

urlpatterns = [

        # Transportation
        url(r'^$', WaypointView.as_view(), name='transport'),
        url(r'^(?P<waypoint_id>\d+)$', WaypointView.as_view(), 
            name='transport-comments'),
        url(r'^(?P<waypoint_id>\d+)/comments$', AddComments.as_view(), 
            name='add-comments'),
        
]
