from urllib2 import URLError

from django.views.generic import ListView

from transport.models import TransportLink

class TransportationView(ListView):
    model = TransportLink