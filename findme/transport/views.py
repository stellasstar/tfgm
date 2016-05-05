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

# not getting waypoints for search_addres
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
        data = {}

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

        # geometry is a gis object.  need to pop out for easier import
        # into data
        position_dict = position.values()[0]
        geometry = position_dict.pop('geometry')
        address = position_dict.pop('address')

        # get address for location
        if address is None:
            (address, city) = mapUtils.get_address_from_latlng(geometry.y, 
                                                               geometry.x)
            position_dict['address'] = address
            position_dict['city'] = city

        # need to fix this, but if there is an addresss but no coordinate info
        if ((geometry is None) or(geometry.x is None) or (geometry.y is None)):
            try:            
                (lat, lng) = mapUtils.get_latlng_from_address(address)
                point = "POINT(%s %s)" % (str(lng), str(lat))
                geometry = geos.fromstr(point)
            except:
                point = "POINT(%s %s)" % (str(settings.DEFAULT_LONGITUDE), 
                                          str(settings.DEFAULT_LATITUDE))
                geometry = geos.fromstr(point)

        if self.request.GET:
            default_address = address.decode('utf-8').lower()
            get_search = self.request.GET.get("search_address")
            search_address = get_search.decode('utf-8').lower()
            if not search_address in default_address: 
                (lat, lng, addy) = mapUtils.get_latlng_from_address(search_address)
                position_dict['address'] = addy
                data['latitude'] = lat
                data['longitude'] = lng
                # default srid used by googlemaps module
                data['srid'] = 4326
            else:
                data['latitude'] = geometry.y
                data['longitude'] = geometry.x
                data['srid'] = geometry.srid
                data['address'] = address

        #update data with user positional data
        data.update(position_dict)        
        
        # where you want the map to be
        data['map'] = self.map_to_show
        data['GOOGLE_KEY'] = self.GOOGLE_KEY
        context['map'] = self.map_to_show

        # get waypoint data
        waypoints, user_location = mapUtils.find_waypoints(geometry.y, geometry.x)

        cls = simplejson.JSONEncoderForHTML
        context['json'] = simplejson.dumps(data, cls=cls)
        context['waypoints'] = waypoints
        context['position'] = position_dict
        context['name'] = name
        context['user'] = user
        context['user_location'] = user_location

        return context


class PositionView(ListView):

    model = Position
