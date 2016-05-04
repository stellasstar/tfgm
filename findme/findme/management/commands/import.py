import os
import findme

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis.gdal import DataSource

from transport.models import (Waypoint, waypoint_mapping, 
                              Route, route_mapping,
                              Area, area_mapping)


class Command(BaseCommand):
    help = 'Loads geospatial data from app data directory'
    route = 'static/data/weogeo/data/public_transport_line.shp'
    wp = 'static/data/weogeo/data/public_transport_point.shp'
    poly = 'static/data/weogeo/data/public_transport_polygon_polygon.shp'
   
    def handle(self, *args, **options):
        route_file = os.path.abspath(os.path.join(os.path.join(os.path.dirname(findme.__file__), self.route)))
        wp_file = os.path.abspath(os.path.join(os.path.join(os.path.dirname(findme.__file__), self.wp)))
        poly_file = os.path.abspath(os.path.join(os.path.join(os.path.dirname(findme.__file__), self.poly)))

        lm1 = LayerMapping(Waypoint, wp_file, waypoint_mapping,
            transform=False, encoding='iso-8859-1')
        lm1.save(strict=True, verbose=True)
        
        lm2 = LayerMapping(Route, route_file, route_mapping,
              transform=False, encoding='iso-8859-1')
        lm2.save(strict=True, verbose=True)

        lm3 = LayerMapping(Area, poly_file, area_mapping,
              transform=False, encoding='iso-8859-1')
        lm3.save(strict=True, verbose=True)

