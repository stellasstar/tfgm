from django.conf.urls import url

from django.contrib import admin
from transport.views import WaypointView


admin.autodiscover()

urlpatterns = [

        # Transportation
        url(r'^$', WaypointView.as_view(), name='transport'),
]
