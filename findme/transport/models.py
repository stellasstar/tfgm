from urllib2 import URLError

from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.core.exceptions import ValidationError


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
    
    
