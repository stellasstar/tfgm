import os

from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

import findme
from transport.models import (Waypoint, waypoint_mapping,
                              Route, route_mapping,
                              Area, area_mapping)

class Command(BaseCommand):
    help = 'Loads geospatial data from app data directory'

    # each file is importing a different set of data
    route = 'static/data/weogeo/data/public_transport_line.shp'
    wp = 'static/data/weogeo/data/public_transport_point.shp'
    poly = 'static/data/weogeo/data/public_transport_polygon_polygon.shp'

    def handle(self, *args, **options):
        route_file = os.path.abspath(os.path.join(
            os.path.join(os.path.dirname(findme.__file__), self.route)))
        wp_file = os.path.abspath(os.path.join(
            os.path.join(os.path.dirname(findme.__file__), self.wp)))
        poly_file = os.path.abspath(os.path.join(
            os.path.join(os.path.dirname(findme.__file__), self.poly)))
        # each LayerMapping object is mapping the data files to its
        # respective model using the *_mapping object
        # usage:  LayerMapping(model, file, file to model mapping
        # transform is False, using the default coordinate system
        # iso-8859-1 specifies the default ASCII character set
        # using the latin alphabet in North America, Western Europe,
        # and Latin America, the Caribbean, Canada, Africa
        # more info about iso is at
        # http://www.w3schools.com/charsets/ref_html_8859.asp

        lm1 = LayerMapping(Waypoint, wp_file, waypoint_mapping,
                           transform=False, encoding='iso-8859-1')
        lm1.save(strict=True, verbose=True)

        lm2 = LayerMapping(Route, route_file, route_mapping,
                           transform=False, encoding='iso-8859-1')
        lm2.save(strict=True, verbose=True)

        lm3 = LayerMapping(Area, poly_file, area_mapping,
                           transform=False, encoding='iso-8859-1')
        lm3.save(strict=True, verbose=True)
