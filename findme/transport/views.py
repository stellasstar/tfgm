from urllib2 import URLError

from django.views.generic import ListView, UpdateView
from leaflet.forms.widgets import LeafletWidget

from transport.models import TransportLink, Position

class TransportationView(ListView):
    model = TransportLink
    
class PositionView(ListView):
    model = Position