from django import forms

from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

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


class WaypointUpdateForm(forms.ModelForm):
    """Form for editing the data that is part of the Waypoint model"""

    class Meta():
        model = Waypoint
        fields = []

    def __init__(self, *args, **kwargs):
        super(WaypointUpdateForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                     'Add Comment',
                                     css_class='btn-primary'))
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

    def save(self, *args, **kwargs):
        user = self.initial['author']
        comment = str(self.cleaned_data['comment'])
        waypoint_id = str(self.data.get('waypoint_id'))
        waypoint = Waypoint.objects.get(pk=waypoint_id)
        new_comment = Comment(
                          waypoint = waypoint,
                          author = user,
                          comment = comment,
                          approved_comment = True
                      )
        new_comment.save()
