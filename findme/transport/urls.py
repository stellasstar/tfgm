from django.conf.urls import url

from django.contrib import admin
from transport.views import WaypointView, AddComments


admin.autodiscover()

urlpatterns = [

        # Transportation
        url(r'^$', WaypointView.as_view(), name='transport'),
        url(r'^pk=(?P<pk>\d+)$', AddComments.as_view(), name='comments'),
        url(r'^pk=(?P<pk>\d+)/comment/$', AddComments.as_view(), name='add_comments'),
        
]
