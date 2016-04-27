import simplejson

from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from django.http import HttpResponseNotFound
from django.conf import settings

from transport.forms import WaypointForm
from transport.models import Waypoint, Position
from transport import mapUtils

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class WaypointView(TemplateView):

    model = Waypoint
    template_name = 'transport/transport.html'
    success_url = "/transport/"
    form_class = WaypointForm
    map_to_show = 'map_canvas'
    GOOGLE_KEY = settings.GOOGLE_API_KEY

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
            raise HttpResponseNotFound
            # Case where user gets to this view
            # anonymously for non-existent user

        if user.is_authenticated():
            position = Position.objects.filter(user=user)
        else:
            raise HttpResponseNotFound

        position_dict = position.values()[0]
        name = position_dict.get('name')

        position_dict = position.values()[0]
        geometry = position_dict.pop('geometry')

        # get address for location
        if position_dict['address'] is None:
            address, city = mapUtils.return_address(geometry.y, geometry.x)
            position_dict['address'] = address
            position_dict['city'] = city

        for key, value in position_dict.iteritems():
            data.append({key: value})

        # this is on purpose, so the json output is easier to read
        data.append({'latitude': geometry.y})
        data.append({'longitude': geometry.x})
        data.append({'srid': geometry.srid})

        # where you want the map to be
        data.append({'map': self.map_to_show})
        data.append({'GOOGLE_KEY': self.GOOGLE_KEY})
        context['map'] = self.map_to_show

        # get waypoint data
        waypoints = mapUtils.find_waypoints(geometry.y, geometry.x)

        cls = simplejson.JSONEncoderForHTML
        context['json'] = simplejson.dumps(data, cls=cls)
        context['waypoints'] = waypoints
        context['position'] = position_dict
        context['name'] = name
        context['user'] = user

        return context


class PositionView(ListView):

    model = Position
