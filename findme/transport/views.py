from urllib2 import URLError

from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.base import TemplateView

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, Http404)
from django.contrib.gis.geos import Point
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.conf import settings
from transport.forms import AddressForm, WaypointForm
from transport.models import Waypoint, Position

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

import json
import simplejson


def geocode_address(address):
    address = address.encode('utf-8')
    geocoder = Google()
    try:
        _, latlon = geocoder.geocode(address)
    except (URLError, GQueryError, ValueError):
        return None
    else:
        return latlon


class WaypointView(TemplateView):

    model = Waypoint
    template_name = 'transport/transport.html'
    success_url = "/transport/"
    form_class = WaypointForm

    def get_context_data(self, **kwargs):
        """
        Load up the default data to
        show in the display form.
        """
        context = super(WaypointView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        position = self.kwargs.get('position')
        data = []

        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            raise Http404
            # Case where user gets to this view
            # anonymously for non-existent user

        if user.is_authenticated():
            position = Position.objects.filter(user=user)
        else:
            raise Http404

        position_dict = position.values()[0]
        name = position_dict.get('name')

        position_dict = position.values()[0]
        geometry = position_dict.pop('geometry')

        for key in position_dict.keys():
            value = position_dict.get(key)
            data.append({key: value})

        data.append({'latitude': geometry.y})
        data.append({'longitude': geometry.x})
        data.append({'srid': geometry.srid})

        # where you want the map to be
        data.append({'map': 'map_canvas'})

        cls = simplejson.JSONEncoderForHTML
        context['map'] = 'map_canvas'
        context['json'] = simplejson.dumps(data, cls=cls)
        context['position'] = position
        context['name'] = name
        context['user'] = user

        return context


class PositionView(ListView):

    model = Position
