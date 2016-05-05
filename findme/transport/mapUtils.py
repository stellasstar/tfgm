import urllib2
from django.conf import settings

from django.core.serializers import serialize as GeoJSONSerializer
from django.contrib.gis.geos import fromstr, GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.gdal import SpatialReference, CoordTransform

from django.contrib.gis.db.models.functions import Distance

import googlemaps, json
from transport.models import Waypoint

# Specify the original srid of your data
orig_srid = 4326


def get_latlng_from_address(a):
    gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    address = u'%s' % (a)
    address = address.encode('utf-8')
    try:
        result = gmap.geocode(address)
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
        addy = result[0]['formatted_address']
    except (urllib2.URLError, urllib2.HTTPError):
        return None
    else:
        return (lat, lng, addy)


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
    user_location = fromstr('POINT(%s %s)' % (lon, lat), srid=4326)
    ct = CoordTransform(SpatialReference("4326"), SpatialReference("3857"))
    user_location.transform(ct)
    radius = 350
    area = (user_location, D(km=0.35))
    # create a polygon object
    circle = user_location.buffer(radius)

    # return everything within area
    waypoints = Waypoint.objects.filter(geom__distance_lte=area)
    # trying to annotate distance
    waypoints.distance(user_location).order_by('distance')
        
    geojson_data = GeoJSONSerializer('geojson',
        waypoints, geometry_field='geom')
    return geojson_data, user_location
