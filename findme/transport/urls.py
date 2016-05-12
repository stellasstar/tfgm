from django.conf.urls import url

from django.contrib import admin
from transport.views import WaypointView, CommentView


admin.autodiscover()

urlpatterns = [

        # Transportation
        url(r'^$', WaypointView.as_view(), name='transport'),
        url(r'^pk=(?P<pk>\d+)$', CommentView.as_view(), name='comments'),
        url(r'^pk=(?P<pk>\d+)/comment/$', CommentView.add_comment_to_post, name='add_comment_to_post'),
        
]
