from django.conf.urls import url

from django.contrib import admin
from transport.views import WaypointView, WaypointAddView, CommentsView


admin.autodiscover()

urlpatterns = [

    # Main
    url(r'^$', WaypointView.as_view(), name='transport'),
    
    # Waypoints
    url(r'^add/$', WaypointAddView.as_view(), name='transport-add'),
    url(r'^update/$', WaypointAddView.as_view(), name='transport-update'),
    url(r'^(?P<waypoint_id>\d+)$', WaypointView.as_view(),
        name='transport-comments'),
    
    # Comments
    url(r'^(?P<waypoint_id>\d+)/comments$', CommentsView.as_view(), 
        name='comments'),

]
