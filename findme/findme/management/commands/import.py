from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from django.conf import settings

from transport.models import Waypoint, waypoint_mapping


class Command(BaseCommand):
    help = 'Loads transport data from app data directory'

    def handle(self, *args, **options):
        waypoint_shp = settings.STATIC_URL + 'data/test.txt'
        lm = LayerMapping(Waypoint, waypoint_shp, waypoint_mapping,
                          transform=False, encoding='iso-8859-1')
        lm.save(strict=True, verbose=True)
