from urllib2 import URLError

from django.utils.translation import gettext as _
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.conf import settings
import googlemaps
from django.utils import timezone

# import custom user model
try:
    # from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class Poly(gis_models.Model):
    geometry = gis_models.PolygonField()
    objects = gis_models.GeoManager()


class Position(gis_models.Model):

    # Relations
    user = models.ForeignKey(User,
                             related_name='owned_positions',
                             null=True,
                             blank=True)
    # postion of user
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    geometry = gis_models.PointField(u"longitude/latitude",
                                     geography=True,
                                     blank=True,
                                     null=True,
                                     srid=4326)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __str__(self):
        return '%s %s %s' % (self.name, self.geometry.x, self.geometry.y)

    def save(self, **kwargs):
        if self.address and not self.geometry:
            gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            try:
                result = gmaps.geocode(address)
                placemark = result['Placemark'][0]
                self.longitude, self.latitude = placemark['Point']['coordinates'][0:2]  
                point = "POINT(%s %s)" % (str(self.longitude), str(self.latitude))
                self.geometry = geos.fromstr(point)                
            except (URLError, GeocoderQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (str(self.longitude), str(self.latitude))
                self.geometry = geos.fromstr(point)
        super(Position, self).save()

    def get_geometry(self):
        return self.geometry

    def get_name(self):
        return self.name


# This is an auto-generated Django model module created by ogrinspect.
# python manage.py ogrinspect findme/static/data/waypoints-new-zealand.gpx \
# Waypoint --srid=4326 --mapping --multi

class Waypoint(gis_models.Model):
    ele = gis_models.FloatField(null=True, blank=True, default=None)
    time = gis_models.DateTimeField(blank=True, default=timezone.now())
    magvar = gis_models.FloatField(null=True, blank=True, default=None)
    geoidheight = gis_models.FloatField(null=True, blank=True, default=None)
    name = gis_models.CharField(max_length=1024, blank=True)
    cmt = gis_models.CharField(max_length=1024, blank=True)
    desc = gis_models.CharField(max_length=1024, blank=True)
    src = gis_models.CharField(max_length=1024, blank=True)
    link1_href = gis_models.CharField(max_length=1024, blank=True)
    link1_text = gis_models.CharField(max_length=1024, blank=True)
    link1_type = gis_models.CharField(max_length=1024, blank=True)
    link2_href = gis_models.CharField(max_length=1024, blank=True)
    link2_text = gis_models.CharField(max_length=1024, blank=True)
    link2_type = gis_models.CharField(max_length=1024, blank=True)
    sym = gis_models.CharField(max_length=1024, blank=True)
    type = gis_models.CharField(max_length=1024, blank=True)
    fix = gis_models.CharField(max_length=1024, blank=True)
    sat = gis_models.IntegerField(null=True, blank=True, default=None)
    hdop = gis_models.FloatField(null=True, blank=True, default=None)
    vdop = gis_models.FloatField(null=True, blank=True, default=None)
    pdop = gis_models.FloatField(null=True, blank=True, default=None)
    ageofdgpsdata = gis_models.FloatField(null=True, blank=True, default=None)
    dgpsid = gis_models.IntegerField(null=True, blank=True, default=None)
    gpxx_waypointextension = gis_models.CharField(max_length=1024, blank=True)
    geom = gis_models.MultiPointField(geography=True,
                                     blank=True,
                                     null=True,
                                     srid=4326)

    class Meta:
        verbose_name = _('waypoint')
        verbose_name_plural = _('waypoints')

    def __unicode__(self):
        return "Waypoint %s" % (self.name)

    def get_lat_long(self):
        """Add an easy getter function, which returns the location coords in
        latitude longitude order
        """
        return (self.geom.coords[1], self.geom.coords[0])


# Auto-generated `LayerMapping` dictionary for Waypoint model
waypoint_mapping = {
    'ele' : 'ele',
    'time' : 'time',
    'magvar' : 'magvar',
    'geoidheight' : 'geoidheight',
    'name' : 'name',
    'cmt' : 'cmt',
    'desc' : 'desc',
    'src' : 'src',
    'link1_href' : 'link1_href',
    'link1_text' : 'link1_text',
    'link1_type' : 'link1_type',
    'link2_href' : 'link2_href',
    'link2_text' : 'link2_text',
    'link2_type' : 'link2_type',
    'sym' : 'sym',
    'type' : 'type',
    'fix' : 'fix',
    'sat' : 'sat',
    'hdop' : 'hdop',
    'vdop' : 'vdop',
    'pdop' : 'pdop',
    'ageofdgpsdata' : 'ageofdgpsdata',
    'dgpsid' : 'dgpsid',
    'gpxx_waypointextension' : 'gpxx_WaypointExtension',
    'geom' : 'MULTIPOINT',
}
