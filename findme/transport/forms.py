from django import forms
from django.conf import settings
from django.contrib import messages

from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from transport.mixin import ReadOnlyFieldsMixin
from transport.models import Waypoint, Comment

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class WaypointForm(forms.ModelForm):
    """Form for creating the data that is part of the Waypoint model"""

    class Meta():
        model = Waypoint
        fields = []

    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(*args, **kwargs)

class WaypointAddForm(forms.ModelForm):
    """Form for creating the data that is part of the Waypoint model"""

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
        fields = ['coffee',
                  'steps',
                  'ramp',
                  'lift',
                  'level_access',
                  'audio_assistance',
                  'audio_talking_description',
                 ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                    'Submit',
                                    css_class='btn-primary'))
        super(WaypointAddForm, self).__init__(*args, **kwargs)


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
