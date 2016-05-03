import urllib2
from django.conf import settings
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.contrib.gis.geos import Point, GEOSGeometry, fromstr, LineString
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.gdal import SpatialReference, CoordTransform

import googlemaps
from transport.models import Waypoint, Route, Area

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
    user_location = fromstr('POINT(%s %s)' % (lon, lat), srid=4326)
    ct = CoordTransform(SpatialReference("4326"), SpatialReference("3857"))
    user_location.transform(ct)
    radius = 2
    area = (user_location, D(km=1))
    # create a polygon object
    circle = user_location.buffer(radius)
    
    # return everything within 1km
    waypoints = Waypoint.objects.filter(geom__distance_lte=area)
    # trying to annotate distance
    waypoints.distance(user_location).order_by('distance')
    geojson_data = GeoJSONSerializer().serialize(
        waypoints, use_natural_keys=True)

    return geojson_data, user_location


