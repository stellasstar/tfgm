import os, csv, sys

from django.core.management.base import BaseCommand
from osgeo import gdal, ogr

import findme
from transport.models import Waypoint


class Command(BaseCommand):

    help = 'Converts geospatial shp file to a csv file'
    shp=r'static/data/weogeo/data/public_transport_point.shp'
    csv_out=r'static/data/weogeo/data/public_transport_point.csv'

    def handle(self, *args, **options):

        shp_file = os.path.abspath(os.path.join(
            os.path.join(os.path.dirname(findme.__file__), self.shp)))
        csv_file = os.path.abspath(os.path.join(
            os.path.join(os.path.dirname(findme.__file__), self.csv_out)))

        #Open files
        csvfile = open(csv_file,'wb')
        ds = ogr.Open(shp_file)
        lyr = ds.GetLayer()
        crs = lyr.GetSpatialRef()

        #Get field names
        dfn = lyr.GetLayerDefn()
        nfields = dfn.GetFieldCount()
        fields = []

        for i in range(nfields):
            fields.append(dfn.GetFieldDefn(i).GetName())
        fields.append('kmlgeometry')
        csvwriter = csv.DictWriter(csvfile, fields)
        try:
            csvwriter.writeheader() #python 2.7+
        except:
            csvfile.write(','.join(fields)+'\n')

        # Write attributes and kml out to csv
        for feat in lyr:
            attributes=feat.items()
            geom=feat.GetGeometryRef()
            print geom.Centroid().ExportToWkt()
            attributes['kmlgeometry']=geom.ExportToWkt()
            csvwriter.writerow(attributes)

        #clean up
        del csvwriter,lyr,ds
        csvfile.close()

