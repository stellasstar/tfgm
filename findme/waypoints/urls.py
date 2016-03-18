from django.conf.urls import patterns, url, include


from waypoints import views

urlpatterns = [
    url(r'^$', views.index, name='waypoints-index'),
    url(r'^save$', views.save, name='waypoints-save'),
    url(r'^search$', views.search, name='waypoints-search'),
    ]