from django import forms
from transport.models import Position, Waypoint


class AddressForm(forms.Form):
    address = forms.CharField()
    model = Position


class WaypointForm(forms.ModelForm):
    """Form for creating the data that is part of the Waypoint model"""

    class Meta():
        model = Waypoint
        fields = ['name',
                  'address',
                  'city',
                  'latitude',
                  'longitude',
                  ]

    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(*args, **kwargs)


class WaypointUpdateForm(forms.ModelForm):
    """Form for editing the data that is part of the Waypoint model"""

    class Meta():
        model = Waypoint
        fields = ['name',
                  'address',
                  'city',
                  'latitude',
                  'longitude',
                  ]

    def __init__(self, *args, **kwargs):
        super(WaypointUpdateForm, self).__init__(*args, **kwargs)
