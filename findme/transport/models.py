from urllib2 import URLError

from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# import custom user model
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User 


class Poly(gis_models.Model):
    geometry = gis_models.PolygonField()
    objects = gis_models.GeoManager()


class TransportLink(gis_models.Model):
    name = models.CharField(max_length=200)
    geom = gis_models.PointField()
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name
    
    def get_lat_long(self):
        """Add an easy getter function, which returns the geometry coords in
        latitude longitude order
        """
        return (self.geom.coords[1], self.geom.coords[0])  
    
    
class Position(gis_models.Model):
    # Relations
    user = models.ForeignKey(User, related_name='owner', null=True, blank=True)
    # postion of user
    name = models.CharField(max_length=32)
    geometry = gis_models.PointField(srid=4326)
    objects = gis_models.GeoManager()

    def __str__(self):
        return '%s %s %s' % (self.name, self.geometry.x, self.geometry.y)
    
    