import os

from django.core.management.base import BaseCommand
from django.conf import settings

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import MultiPoint, fromstr

import findme
from transport.models import Waypoint

# waypoint_mapping = {
# 'osm_id' : 'OSM_ID',
# 'public_tra' : 'PUBLIC_TRA',
# 'name' : 'NAME',
# 'ref' : 'REF',
# 'route_ref' : 'ROUTE_REF',
# 'operator' : 'OPERATOR',
# 'network' : 'NETWORK',
# 'train' : 'TRAIN',
# 'subway' : 'SUBWAY',
# 'monorail' : 'MONORAIL',
# 'tram' : 'TRAM',
# 'bus' : 'BUS',
# 'trolleybus' : 'TROLLEYBUS',
# 'aerialway' : 'AERIALWAY',
# 'ferry' : 'FERRY',
# 'shelter' : 'SHELTER',
# 'bench' : 'BENCH',
# 'covered' : 'COVERED',
# 'area' : 'AREA',
# 'z_order' : 'Z_ORDER',
# 'geom' : 'MULTIPOINT25D',
# }

# example input data
# OSM_ID,PUBLIC_TRA,NAME,REF,ROUTE_REF,OPERATOR,NETWORK,TRAIN,SUBWAY,
# MONORAIL,TRAM,BUS,TROLLEYBUS,AERIALWAY,FERRY,SHELTER,BENCH,
# COVERED,AREA,Z_ORDER,kmlgeometry
# 3974050131.0,stop_position,,,,,,,,,,yes,,,,,,,,,
# POINT (-219133.54 7045434.48 0)


class Command(BaseCommand):
    help = 'Loads Tfgm geospatial data from app data directory'
    wp = 'static/data/weogeo/data/public_transport_point.csv'

    # using 2 different coordinate transformation systems for better accuracy
    # 27700 corresponds to the British National Grid coordinate system
    # 4326 corresponds to the U.S. Department of Defense, and is the
    #     standard used by the Global Positioning System (GPS)
    # 3857 corresponds to Web Mercator and is the standard for Web
    #     mapping applications
    # bng is the British National Grid
    # web_transform is transforming to web standards

    def handle(self, *args, **options):
        wp_file = os.path.abspath(os.path.join(os.path.join(
                      os.path.dirname(findme.__file__), self.wp)))
        f = open(wp_file, 'r')
        user = User.objects.get(username = 'transport')
        fields = Waypoint._meta.get_fields()
        for line in f:
            words = line.split(",")
            w = Waypoint.objects.create(user=user)
            coords = words.pop(-1)
            location = fromstr(coords.strip(),
                               srid=settings.WEB_MERCATOR_STANDARD)
            w.z_order = '0.0'
            w.geom = MultiPoint(location)
            w.osm_id = words[0]
            w.public_tra = words[1]
            
            print w.id, w
            w.save()

        f.close()
