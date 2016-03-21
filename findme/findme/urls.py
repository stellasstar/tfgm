from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
              url(r'^admin/', include(admin.site.urls)),
              url(r'', include('waypoints.urls'), name="waypoints"),
              url(r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'findme/login.html'})
]
