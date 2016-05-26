from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.gis import forms as gis_forms
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Count, F

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
import floppyforms

from transport import choices
from transport.mixin import ReadOnlyFieldsMixin
from transport.models import Waypoint, Comment, Area, Route

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# import manchester area
MANC = Area.objects.get(name='Greater Manchester')


class GmapPointWidget(floppyforms.gis.BaseGMapWidget,
                           floppyforms.gis.PointWidget):
    map_srid = settings.WEB_MERCATOR_STANDARD
    required = True
    display_wkt = False
    default_lon = settings.DEFAULT_WEB_LATITUDE
    default_lat = settings.DEFAULT_WEB_LONGITUDE

    def get_context_data(self):
        ctx = super(GmapPointWidget, self).get_context_data()
        ctx.update({
            'lon': self.default_lon,
            'lat': self.default_lat,
        })
        return ctx

class WaypointForm(forms.ModelForm):
    """Form for creating the data that is part of the Waypoint model"""

    class Meta():
        model = Waypoint
        fields = []

    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(*args, **kwargs)


class WaypointAddForm(forms.ModelForm):
    """Form for creating the data that is part of the Waypoint model"""

    area_target = floppyforms.gis.PointField(widget=GmapPointWidget)

    name = forms.CharField(error_messages={'required': 'Please enter a name'})
    steps = forms.ChoiceField(choices=[(x, x) for x in range(0, 350)])
    coffee = forms.ChoiceField(choices=[(x, x) for x in range(0, 350)],
                help_text='Distance from stop in metres.')
    public_tra = forms.ChoiceField(choices=choices.STOP_TYPES, 
                     required=True, label='Type of stop')
    area = forms.ModelChoiceField(
        queryset=Area.objects.annotate(
        area_count=Count('name')))
    
    route_ref = forms.ModelChoiceField(
            queryset=Route.objects.annotate(
            route_count=Count('name')))

    class Meta():
        model = Waypoint
        fields = ['area_target',
                  'name',
                  'ref',
                  'operator',
                  'network',
                  'coffee',
                  'steps',
                  'ramp',
                  'lift',
                  'level_access',
                  'audio_assistance',
                  'audio_talking_description',
                  'shelter',
                  'bench',
                  'covered'
                 ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                    'Submit',
                                    css_class='btn btn-default'))
        super(WaypointAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        user = self.initial['author']
        new_waypoint = super(WaypointAddForm, self).save(commit=False)
        new_waypoint = Waypoint.objects.create(wp_owner = user)
        new_waypoint.name = name
        new_waypoint.public_tra = public_tra
        new_waypoint.ref = ref
        new_waypoint.route_ref = route_ref
        new_waypoint.operator = operator
        new_waypoint.network = network
        new_waypoint.coffee = coffee
        new_waypoint.steps = steps
        new_waypoint.ramp = ramp
        new_waypoint.lift = lift
        new_waypoint.level_access = level_access
        new_waypoint.audio_assistance = audio_assistance
        new_waypoint.audio_talking_description = audio_talking_description
        new_waypoint.shelter = shelter
        new_waypoint.bench = bench
        new_waypoint.covered = covered
        new_waypoint.save()
        return new_waypoint


class WaypointUpdateForm(forms.ModelForm):
    """Form for editing the data that is part of the Waypoint model"""

    steps = forms.ChoiceField(choices=[(x, x) for x in range(1, 350)])
    coffee = forms.ChoiceField(choices=[(x, x) for x in range(1, 350)])
    ramp = forms.BooleanField(required=False,initial=False,label='ramp')
    lift = forms.BooleanField(required=False,initial=False,label='lift')
    level_access = forms.BooleanField(required=False,
                                      initial=False,label='level_access')
    audio_assistance = forms.BooleanField(required=False,
                                          initial=False,label='audio_assistance')
    audio_talking_description = forms.BooleanField(required=False,
                                                   initial=False,label='audio_talking_description')

    class Meta():
        model = Waypoint
        fields = []

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                     'Update',
                                     css_class='btn-primary'))
        super(WaypointUpdateForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'size': '40'}),
        error_messages={'required': 'There needs to be a comment to save.'})

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FormActions(
                Submit('submit', 'Add', 
                       css_class="btn-default"),
                Submit('edit', 'Edit', 
                       css_class="btn-default"),
                Submit('cancel', 'Cancel', 
                       css_class="btn-default"),),
        )
        super(CommentForm, self).__init__(*args, **kwargs)

    def get_comments(self, waypoint_id):
        waypoint = Waypoint.objects.get(pk=waypoint_id)
        comments = waypoint.wp_comments.all().order_by('created_date')
        return (waypoint, comments)

    def get_context_data(self, **kwargs):
        waypoint_id = kwargs['waypoint_id']
        (waypoint, comments) = self.get_comments(pk=waypoint_id)
        context['comments'] = comments
        context['waypoint_id'] = waypoint_id
        return context
    
    def save(self, commit=True, *args, **kwargs):
        user = self.initial['author']
        comment = self.cleaned_data['comment']
        waypoint_id = str(self.data.get('waypoint_id'))
        waypoint = Waypoint.objects.get(pk=waypoint_id)
        new_comment = super(CommentForm, self).save(commit=False)
        new_comment.waypoint = waypoint
        new_comment.author = user
        new_comment.comment = comment
        new_comment.approved_comment = True
        new_comment.save()
        return new_comment
