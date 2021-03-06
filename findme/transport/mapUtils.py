import urllib2
from django.conf import settings

from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.gdal import SpatialReference, CoordTransform

import googlemaps
from djgeojson.serializers import Serializer as GeoJSONSerializer

from transport.models import Waypoint


def get_latlng_from_address(a):
    gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    address = u'%s' % (a)
    address = address.encode('utf-8')
    try:
        result = gmap.geocode(address)
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
        addy = result[0]['formatted_address']
        city = result[0]['address_components'][4]['long_name']
    except (urllib2.URLError, urllib2.HTTPError):
        return None
    else:
        return [lat, lng, addy, city]


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
    user_location = fromstr('POINT(%s %s)' % (lon, lat),
                            srid=settings.US_DOD_GPS)
    ct = CoordTransform(
            SpatialReference(settings.US_DOD_GPS),
            SpatialReference(settings.WEB_MERCATOR_STANDARD))
    user_location.transform(ct)
    area = (user_location, D(km=0.35))

    # return everything within area
    waypoints = Waypoint.objects.filter(geom__distance_lte=area)
    # trying to annotate distance
    waypoints.distance(user_location).order_by('distance')

    geojson_data = GeoJSONSerializer().serialize(
                      waypoints, use_natural_keys=True)
    return geojson_data, user_location
