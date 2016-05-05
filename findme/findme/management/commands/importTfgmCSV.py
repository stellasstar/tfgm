import inspect, sys, csv, os, re
import findme

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis.gdal import DataSource

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import (Point, GEOSGeometry, MultiPoint, 
                                     fromstr, LineString)

from djgeojson.serializers import Serializer as GeoJSONSerializer

from transport.models import Waypoint

#waypoint_mapping = {
    #'osm_id' : 'OSM_ID',
    #'public_tra' : 'PUBLIC_TRA',
    #'name' : 'NAME',
    #'ref' : 'REF',
    #'route_ref' : 'ROUTE_REF',
    #'operator' : 'OPERATOR',
    #'network' : 'NETWORK',
    #'train' : 'TRAIN',
    #'subway' : 'SUBWAY',
    #'monorail' : 'MONORAIL',
    #'tram' : 'TRAM',
    #'bus' : 'BUS',
    #'trolleybus' : 'TROLLEYBUS',
    #'aerialway' : 'AERIALWAY',
    #'ferry' : 'FERRY',
    #'shelter' : 'SHELTER',
    #'bench' : 'BENCH',
    #'covered' : 'COVERED',
    #'area' : 'AREA',
    #'z_order' : 'Z_ORDER',
    #'geom' : 'MULTIPOINT25D',
#}

# AtcoCode,,Easting,Northing,CommonName,Indicator,Bearing,Street,Landmark,NptgLocalityCode,,,StopType,BusStopType,TimingStatus,Status,RevisionNumber,Notes,LocalityCentre,NaptanCode,ShortCommonName,ModificationDate
#['"1800AMIC001"', '""', '376969', '387893', '"Altrincham Interchange"', '"Nr Train Station"', '"NA"', '"STAMFORD NE
#W RD"', '"Altrincham Interchange"', '"E0028261"', '""', '""', '"BCS"', '"MKD"', '"TIP"', '"ACT"', '17', '"STOP BB R
#EMOVED FROM AMIC"', '"Y"', '"MANADADG"', '"Interchange"', '"2014-12-18"\r\n']

class Command(BaseCommand):
    help = 'Loads Tfgm geospatial data from app data directory'
    wp = 'static/data/TfGMStoppingPoints.csv'
    
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
        f = open(wp_file, 'r');
        bng = CoordTransform(SpatialReference("27700"), 
                             SpatialReference("4326"))
        web_transform = CoordTransform(SpatialReference("4326"), 
                        SpatialReference("3857"))        
        for line in f:
            words = line.split(",");
            w = Waypoint.objects.create()
            easting = words[2]
            northing = words[3]
            location = fromstr('POINT(%s %s)' % (easting, northing), srid=27700)
            location.transform(bng)
            location.transform(web_transform)
            w.geom = MultiPoint(location)
            w.bus = 'yes'
            w.name = words[4].strip('"')
            w.indicator = words[5].strip('"')
            w.ref = words[0].strip('"')
            w.public_tra = 'stop_position'
            w.area = words[9].strip('"')
            w.route_ref = words[9].strip('"')
            w.z_order = '0.0'
            print w
            w.save()
            
        f.close()
