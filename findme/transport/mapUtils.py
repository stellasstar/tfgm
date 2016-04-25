from django.conf import settings
from django.contrib.gis.geos import Point
from djgeojson.serializers import Serializer as GeoJSONSerializer

import googlemaps
from transport.forms import WaypointForm
from transport.models import Waypoint, Position


def geocode_address(address):
    googlemaps.Client(key=settings.GOOGLE_API_KEY)
    address = u'%s %s' % (self.address, self.city)
    address = address.encode('utf-8')
    try:
        result = gmaps.geocode(address)
        placemark = result['Placemark'][0]
        lng, lat = placemark['Point']['coordinates'][0:2]  
        latlon = (lat, lng)
    except (URLError, GeocoderQueryError, ValueError):
        return None
    else:
        return latlon

def return_address(lat, lng):
    latlng = (lat, lng)
    gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    try:
        reverse = gmap.reverse_geocode(latlng)
        addy = reverse[0].get('formatted_address')
        city = reverse[0].get('address_components')[3].get('long_name')
        return addy, city
    except:
        pass


def find_waypoints(lat, lon):
    """
    Given a given lat/long pair, return the unit(s) surrounding it.
    """
    
    point = Point(float(lon), float(lat))
    waypoints = Waypoint.objects.order_by('name')
    geojson_data = GeoJSONSerializer().serialize(
        waypoints, use_natural_keys=True) 

    return geojson_data