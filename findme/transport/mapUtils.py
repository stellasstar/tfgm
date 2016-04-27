import urllib2
from django.conf import settings
from djgeojson.serializers import Serializer as GeoJSONSerializer

import googlemaps
from transport.models import Waypoint


def get_latlng_from_address(a):
    gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    address = u'%s' % (a)
    address = address.encode('utf-8')
    try:
        result = gmap.geocode(address)
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
    except (urllib2.URLError, urllib2.HTTPError):
        return None
    else:
        return (lat, lng)


def get_address_from_latlng(lat, lng):
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
    Given a given lat/long pair, return the waypoint(s) surrounding it.
    """

    waypoints = Waypoint.objects.order_by('name')
    geojson_data = GeoJSONSerializer().serialize(
        waypoints, use_natural_keys=True)

    return geojson_data
