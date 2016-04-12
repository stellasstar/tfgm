from django import forms
from django.views.generic import ListView, UpdateView
from leaflet.forms.widgets import LeafletWidget

from transport.models import Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        widgets = {'geometry': LeafletWidget()}


class EditPositionForm(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'position.html'

