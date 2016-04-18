from urllib2 import URLError

from django.utils.translation import gettext as _
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from geopy.geocoders.googlev3 import GoogleV3
from geopy.geocoders.googlev3 import GeocoderQueryError
# import custom user model
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User 


class Poly(gis_models.Model):
    geometry = gis_models.PolygonField()
    objects = gis_models.GeoManager()


class Waypoint(gis_models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)  
    latitude = models.DecimalField(max_digits=10,
                                   decimal_places=6,
                                   null=True)
    longitude = models.DecimalField(max_digits=10,
                                    decimal_places=6,
                                    null=True)      
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True,srid=4326)
    
    gis = gis_models.GeoManager()
    objects = models.Manager()
    
    gis.filter() # with GIS queries
    objects.filter() # only standard queries    
    
    class Meta:
        verbose_name = _('waypoint')
        verbose_name_plural = _('waypoints') 
    
    def __unicode__(self):
        return self.name

    def get_lat_long(self):
        """Add an easy getter function, which returns the location coords in
        latitude longitude order
        """
        return (self.location.coords[1], self.location.coords[0])

    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = Google()
            try:
                _, latlon = geocoder.geocode(address)
            except (URLError, GQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = geos.fromstr(point)
        super(Waypoint, self).save()


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
        if not self.geometry:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = GoogleV3()
            try:
                _, latlon = geocoder.geocode(address)
            except (URLError, GeocoderQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.geometry = geos.fromstr(point)
        super(Position, self).save()

    def get_geometry(self):
        return self.geometry

    def get_name(self):
        return self.name


# Auto-generated `LayerMapping` dictionary for Waypoint model
waypoint_mapping = {
    'name': 'Name',
    'longitude': 'Longitude',
    'latitude': 'Latitude',
    'address': 'Address',
    'city': 'City',
    'location': 'UNKNOWN',
}
