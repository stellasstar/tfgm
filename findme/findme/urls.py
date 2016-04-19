from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from findme.views import HomePageView, ContactFormView, StaticView
from django.conf import settings
from django.views import defaults as default_views

admin.autodiscover()

urlpatterns = [
            # index page
            url(r'^$', HomePageView.as_view(), name='home'),
            url(r'^contact/$', ContactFormView.as_view(), name='contact'),
            url(r'^(?P<page>.+\.html)$', StaticView.as_view()),
            url(r'^gatekeeper/', include('gatekeeper.urls')),
            url(r'^transport/', include('transport.urls')),

            # Uncomment the next line to enable the admin:
            url(r'^admin/', include(admin.site.urls)),

            # Uncomment the admin/doc line below to enable admin documentation:
            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Other url patterns ...
if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
    ]
