from django import forms
from django.contrib.gis.geos import Point
from waypoints.models import PointEntry


class PointEntryForm(forms.ModelForm):

    latitude = forms.DecimalField(
        min_value=-90,
        max_value=90,
        required=True,
    )
    longitude = forms.DecimalField(
        min_value=-180,
        max_value=180,
        required=True,
    )

    class Meta(object):
        model = PointEntry
        exclude = []
        widgets = {'point': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        if args:    # If args exist
            data = args[0]
            if data['latitude'] and data['longitude']:    #If lat/lng exist
                latitude = float(data['latitude'])
                longitude = float(data['longitude'])
                data['point'] = Point(longitude, latitude)    # Set PointField
        try:    
            coordinates = kwargs['instance'].point.tuple    #If PointField exists 
            initial = kwargs.get('initial', {})    
            initial['latitude'] = coordinates[0]    #Set Latitude from coordinates
            initial['longitude'] = coordinates[1]    #Set Longitude from coordinates
            kwargs['initial'] = initial
        except (KeyError, AttributeError):
            pass
        super().__init__(*args, **kwargs)