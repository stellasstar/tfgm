import simplejson


from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import QueryDict

from django.views.generic import ListView, CreateView

from django.views.generic.base import TemplateView

from transport.forms import WaypointForm, CommentForm
from transport.models import Waypoint, Position, Comment
from transport import mapUtils

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


# home button in search address is not working
class WaypointView(TemplateView):

    model = Waypoint
    template_name = 'transport/transport.html'
    success_url = "/transport/"
    form_class = WaypointForm
    map_to_show = 'map_canvas'
    GOOGLE_KEY = settings.GOOGLE_API_KEY

    def get_comments(self, pk):
        waypoint = Waypoint.objects.get(pk=pk)
        comments = Comment.objects.filter(
                   post=waypoint).order_by('created_date')
        return (waypoint, comments)

    def get_inital_user_data(self):

        data = {}
        position = Position.objects.filter(user=self.request.user).last()

        geometry = position.geometry

        # get address for location
        if position.address is None:
            (address, city) = mapUtils.get_address_from_latlng(geometry.y,
                                                               geometry.x)
            data['address'] = address
            data['city'] = city
        else:
            data['address'] = position.address
            data['city'] = position.city

        # need to fix this, but if there is an addresss but no coordinate info
        if ((geometry is None) or(geometry.x is None) or (geometry.y is None)):
            try:
                results = mapUtils.get_latlng_from_address(data['address'])
                data['latitude'] = results[0]
                data['longitude'] = results[1]
                data['address'] = results[2]
                data['city'] = results[3]
            except:
                msg = "Can't find coordinates, setting to default"
                messages.error(self.request, msg)
                data['latitude'] = settings.DEFAULT_LONGITUDE
                data['longitude'] = settings.DEFAULT_LATITUDE
        else:
            data['latitude'] = geometry.y
            data['longitude'] = geometry.x

        data['srid'] = geometry.srid
        data['name'] = position.name

        # where you want the map to be
        data['map'] = self.map_to_show
        data['GOOGLE_KEY'] = self.GOOGLE_KEY

        # populate the initial session data
        self.request.session['data'] = data
        return data

    def get_context_data(self, **kwargs):

        """
        Load up the default data to
        show in the display form.
        """
        context = super(WaypointView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        data = {}
        comments = []
        waypoint = []

        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
            searched = self.request.session.get('searched', None)
            if searched is None or searched is False:
                data = self.get_inital_user_data()
            else:
                data = self.request.session.get('data')
        else:
            user = User
        context['user'] = user

        # searching for the information in the address search bar
        # home button in search address is not working
        if self.request.GET.get("search_address"):
            # remove old waypoint information
            kwargs.pop('waypoint_id')
            context.pop('waypoint_id')
            context.pop('comments')

            # get new area waypoint data
            self.request.session['searched'] = True
            default_address = data['address'].decode('utf-8').lower()
            get_search = self.request.GET.get("search_address")
            search_address = get_search.decode('utf-8').lower()
            if search_address not in default_address:
                try:
                    results = mapUtils.get_latlng_from_address(search_address)
                    data['latitude'] = results[0]
                    data['longitude'] = results[1]
                    data['address'] = results[2]
                    data['city'] = results[3]
                    self.request.session['data'] = data
                except Exception as e:
                    exc = "Exception: " + str(e)
                    msg = "Can't find search address. " + search_address
                    messages.error(self.request, msg)
                    messages.add_message(self.request, messages.ERROR, exc)
                    data = self.request.session['data']

        waypoint_id = str(self.kwargs.get('waypoint_id'))
        location_id = self.request.GET.get('location_id')
        context['location_id'] = location_id
        (waypoint, comments) = self.get_comments(waypoint_id)
        # for comments about individual waypoints
        context['comments'] = comments
        context['waypoint'] = waypoint

        # get waypoint data
        waypoints, user_location = mapUtils.find_waypoints(data['latitude'],
                                                           data['longitude'])

        cls = simplejson.JSONEncoderForHTML
        context['json'] = simplejson.dumps(data, cls=cls)
        context['waypoints'] = waypoints
        context['map'] = self.map_to_show

        return context


class PositionView(ListView):

    model = Position


class AddComments(CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'transport/comments.html'

    def get_success_url(self):
        return reverse('add-comments', kwargs={
            'waypoint_id': self.kwargs.get('waypoint_id')})

    def get_context_data(self, **kwargs):
        context = super(AddComments, self).get_context_data(**kwargs)
        waypoint_id = str(self.kwargs.get('waypoint_id'))
        waypoint = Waypoint.objects.get(pk=waypoint_id)
        comments = Comment.objects.filter(post=waypoint).order_by('created_date')
        context['comments'] = comments
        context['waypoint_id'] = waypoint_id
        context['waypoint'] = waypoint
        return context
    
    