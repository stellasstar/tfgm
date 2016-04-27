import os
import findme

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.conf import settings
from django.conf.urls.static import static

from transport.models import Waypoint, waypoint_mapping


class Command(BaseCommand):
    help = 'Loads geospatial data from app data directory'
    fileToLoad = 'static/data/bus/bus-stops/data/BusRouteMapData/KML-format/OpenData_BusRoutes.KML'

    def handle(self, *args, **options):
        waypoint_shp = os.path.abspath(os.path.join(os.path.join(os.path.dirname(findme.__file__), self.fileToLoad)))

        lm = LayerMapping(Waypoint, waypoint_shp, waypoint_mapping, 
            transform=False, encoding='iso-8859-1') 
        lm.save(strict=True, verbose=True)
