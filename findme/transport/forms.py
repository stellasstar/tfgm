from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from transport.models import Waypoint, Comment


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
        fields = ['author',
                  'text',
                 ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',
                                     'Add Comment',
                                     css_class='btn-primary'))
        super(CommentForm, self).__init__(*args, **kwargs)

    def get_comments(self, pk):
        waypoint = Waypoint.objects.get(pk=pk)
        comments = Comment.objects.filter(post=waypoint)
        return (waypoint, comments)
        
    def get_context_data(self, **kwargs):
        pk = self.request.GET.get['pk']
        (waypoint, comments) = self.get_comments(pk=pk)
        context['comments'] = comments
        context['pk'] = pk
        return context
    
    def save(self, *args, **kwargs):
        author = str(self.cleaned_data['author'])
        text = str(self.cleaned_data['text'])
        pk = str(self.data.getlist('pk')[0])
        waypoint = Waypoint.objects.get(pk=pk)
        new_comment = Comment(
                          post = waypoint,
                          author = author,
                          text = text,
                          approved_comment = True
                      )
        new_comment.save()
