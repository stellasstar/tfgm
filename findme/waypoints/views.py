from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis.gdal import DataSource
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

# Import system modules
import itertools
import tempfile
import os
# Import custom modules
from waypoints.models import Waypoint
import json

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    waypoints = Waypoint.objects.order_by('name')
    template = loader.get_template('waypoints/index.html')
    context = RequestContext(request, {
        'waypoints': waypoints, 'content': render_to_string('waypoints/waypoints.html', {'waypoints': waypoints})
    })
    return HttpResponse(template.render(context))

@csrf_exempt
################## doesnt work without the @csrf_exempt.  Have to figure out why this is the case#########
def save(request):
    c = {}
    c.update(csrf(request))
    for waypointString in request.POST.get('waypointsPayload', '').splitlines():
        waypointID, waypointX, waypointY = waypointString.split()
        waypoint = Waypoint.objects.get(id=int(waypointID))
        waypoint.geometry.set_x(float(waypointX))
        waypoint.geometry.set_y(float(waypointY))
        waypoint.save()
    return HttpResponse(json.dumps(dict(isOk=1)), c)


def search(request):
    # Build searchPoint
    try:
        searchPoint = Point(float(request.GET.get('lng')), float(request.GET.get('lat')))
    except:
        return HttpResponse(json.dumps(dict(isOk=0, message='Could not parse search point')))
    # Search database
    waypoints = Waypoint.objects.distance(searchPoint).order_by('distance')
    # Return
    return HttpResponse(json.dumps(dict(
        isOk=1,
        content=render_to_string('waypoints/waypoints.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )))

