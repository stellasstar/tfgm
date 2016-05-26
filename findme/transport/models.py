from urllib2 import URLError

import django
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.utils import timezone

from transport import choices

try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User

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

# need to fix save method
    def save(self, **kwargs):
        if self.address and not self.geometry:
            # gmap = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            try:
                # self.longitude, self.latitude =
                # placemark['Point']['coordinates'][0:2]
                point = "POINT(%s %s)" % (str(self.longitude),
                                          str(self.latitude))
                self.geometry = geos.fromstr(point)
            except (URLError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (str(self.longitude),
                                          str(self.latitude))
                self.geometry = geos.fromstr(point)
        super(Position, self).save()

    def get_geometry(self):
        return self.geometry

    def get_name(self):
        return self.name


# This is an auto-generated Django model module created by ogrinspect.
# python manage.py ogrinspect findme/static/data/waypoints-new-zealand.gpx \
# Waypoint --srid=3857 --mapping --multi

class Waypoint(gis_models.Model):

    wp_owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='wp_owner', default=1)
    public_tra = gis_models.CharField(max_length=254, default='stop_position')
    name = gis_models.CharField(max_length=254, default='')
    ref = gis_models.CharField(max_length=254, null=True, blank=True)
    route_ref = gis_models.CharField(max_length=254, null=True, blank=True)
    operator = gis_models.CharField(max_length=254, null=True, blank=True)
    network = gis_models.CharField(max_length=254, null=True, blank=True)
    train = gis_models.BooleanField(default=False)
    subway = gis_models.BooleanField(default=False)
    monorail = gis_models.BooleanField(default=False)
    tram = gis_models.BooleanField(default=False)
    bus = gis_models.BooleanField(default=True)
    trolleybus = gis_models.BooleanField(default=False)
    aerialway = gis_models.BooleanField(default=False)
    ferry = gis_models.BooleanField(default=False)
    shelter = gis_models.BooleanField(default=False)
    bench = gis_models.BooleanField(default=False)
    covered = gis_models.BooleanField(default=False)
    area = gis_models.CharField(max_length=254, null=True, blank=True)
    z_order = gis_models.FloatField(null=True, blank=True)
    geom = gis_models.MultiPointField(blank=True, null=True,
                                      srid=settings.WEB_MERCATOR_STANDARD)
    indicator = gis_models.CharField(max_length=254, null=True, blank=True)

    steps = gis_models.PositiveSmallIntegerField(default=0)
    coffee = gis_models.PositiveSmallIntegerField(default=0)
    ramp = gis_models.BooleanField(default=False)
    lift = gis_models.BooleanField(default=False)
    level_access = gis_models.BooleanField(default=False)
    audio_assistance = gis_models.BooleanField(default=False)
    audio_talking_description = gis_models.BooleanField(default=False)

    #comments = models.ForeignKey('transport.Comment',
                             #related_name='comments_wp',
                             #null=True,
                             #blank=True)
    objects = gis_models.GeoManager()

    class Meta:
        verbose_name = _('waypoint')
        verbose_name_plural = _('waypoints')

    def __unicode__(self):
        return "Waypoint %s" % (self.name)

    def get_lat_long(self):
        return (self.geom.coords[1], self.geom.coords[0])


class Route(gis_models.Model):
    route_owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='route_owner', default=1)
    public_tra = gis_models.CharField(max_length=254, blank=True)
    name = gis_models.CharField(max_length=254, blank=True)
    ref = gis_models.CharField(max_length=254, blank=True)
    route_ref = gis_models.CharField(max_length=254, blank=True)
    operator = gis_models.CharField(max_length=254, blank=True)
    network = gis_models.CharField(max_length=254, blank=True)
    train = gis_models.CharField(max_length=254, blank=True)
    subway = gis_models.CharField(max_length=254, blank=True)
    monorail = gis_models.CharField(max_length=254, blank=True)
    tram = gis_models.CharField(max_length=254, blank=True)
    bus = gis_models.CharField(max_length=254, blank=True)
    trolleybus = gis_models.CharField(max_length=254, blank=True)
    aerialway = gis_models.CharField(max_length=254, blank=True)
    ferry = gis_models.CharField(max_length=254, blank=True)
    shelter = gis_models.CharField(max_length=254, blank=True)
    bench = gis_models.CharField(max_length=254, blank=True)
    covered = gis_models.CharField(max_length=254, blank=True)
    area = gis_models.CharField(max_length=254, blank=True)
    z_order = gis_models.FloatField(blank=True, null=True)
    geom = gis_models.MultiLineStringField(srid=3857, blank=True, null=True)

    objects = gis_models.GeoManager()

    def __unicode__(self):
        return "Route %s" % (self.name)


class Area(gis_models.Model):
    area_owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='area_owner', default=1)
    public_tra = gis_models.CharField(max_length=254, blank=True)
    name = gis_models.CharField(max_length=254, blank=True)
    ref = gis_models.CharField(max_length=254, blank=True)
    route_ref = gis_models.CharField(max_length=254, blank=True)
    operator = gis_models.CharField(max_length=254, blank=True)
    network = gis_models.CharField(max_length=254, blank=True)
    train = gis_models.CharField(max_length=254, blank=True)
    subway = gis_models.CharField(max_length=254, blank=True)
    monorail = gis_models.CharField(max_length=254, blank=True)
    tram = gis_models.CharField(max_length=254, blank=True)
    bus = gis_models.CharField(max_length=254, blank=True)
    trolleybus = gis_models.CharField(max_length=254, blank=True)
    aerialway = gis_models.CharField(max_length=254, blank=True)
    ferry = gis_models.CharField(max_length=254, blank=True)
    shelter = gis_models.CharField(max_length=254, blank=True)
    bench = gis_models.CharField(max_length=254, blank=True)
    covered = gis_models.CharField(max_length=254, blank=True)
    area = gis_models.CharField(max_length=254, blank=True)
    z_order = gis_models.FloatField(null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=3857, blank=True, null=True)

    objects = gis_models.GeoManager()

    def __unicode__(self):
        return "Area %s" % (self.name)

class Comment(models.Model):
    approved_comment = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    waypoint = models.ForeignKey('transport.Waypoint',
                             related_name='wp_comments',
                             null=True,
                             blank=True,)
    position = models.ForeignKey('transport.Position', 
                                 related_name='position_comments',
                                 null=True,
                                 blank=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='author')
    comment = models.TextField(null=True, blank=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment
    

# Auto-generated `LayerMapping` dictionary for Waypoint model
waypoint_mapping = {
    'public_tra': 'PUBLIC_TRA',
    'name': 'NAME',
    'ref': 'REF',
    'route_ref': 'ROUTE_REF',
    'operator': 'OPERATOR',
    'network': 'NETWORK',
    'train': 'TRAIN',
    'subway': 'SUBWAY',
    'monorail': 'MONORAIL',
    'tram': 'TRAM',
    'bus': 'BUS',
    'trolleybus': 'TROLLEYBUS',
    'aerialway': 'AERIALWAY',
    'ferry': 'FERRY',
    'shelter': 'SHELTER',
    'bench': 'BENCH',
    'covered': 'COVERED',
    'area': 'AREA',
    'z_order': 'Z_ORDER',
    'geom': 'MULTIPOINT25D',
}

# Auto-generated `LayerMapping` dictionary for Waypoints model
route_mapping = {
    'public_tra': 'PUBLIC_TRA',
    'name': 'NAME',
    'ref': 'REF',
    'route_ref': 'ROUTE_REF',
    'operator': 'OPERATOR',
    'network': 'NETWORK',
    'train': 'TRAIN',
    'subway': 'SUBWAY',
    'monorail': 'MONORAIL',
    'tram': 'TRAM',
    'bus': 'BUS',
    'trolleybus': 'TROLLEYBUS',
    'aerialway': 'AERIALWAY',
    'ferry': 'FERRY',
    'shelter': 'SHELTER',
    'bench': 'BENCH',
    'covered': 'COVERED',
    'area': 'AREA',
    'z_order': 'Z_ORDER',
    'geom': 'MULTILINESTRING25D',
}


# Auto-generated `LayerMapping` dictionary for Areas model
area_mapping = {
    'public_tra': 'PUBLIC_TRA',
    'name': 'NAME',
    'ref': 'REF',
    'route_ref': 'ROUTE_REF',
    'operator': 'OPERATOR',
    'network': 'NETWORK',
    'train': 'TRAIN',
    'subway': 'SUBWAY',
    'monorail': 'MONORAIL',
    'tram': 'TRAM',
    'bus': 'BUS',
    'trolleybus': 'TROLLEYBUS',
    'aerialway': 'AERIALWAY',
    'ferry': 'FERRY',
    'shelter': 'SHELTER',
    'bench': 'BENCH',
    'covered': 'COVERED',
    'area': 'AREA',
    'z_order': 'Z_ORDER',
    'geom': 'MULTIPOLYGON25D',
}
