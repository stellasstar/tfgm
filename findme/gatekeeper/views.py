from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import parsers, renderers, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from gatekeeper.serializers import *
from gatekeeper.permissions import IsNotAuthenticated, IsProfileOwner


#method decorator
from django.utils.decorators import method_decorator

#import user forms
from gatekeeper.forms import UserRegistrationForm

#import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
class AccountLogin(generics.GenericAPIView):
    """
    Log in
    
    **Parameters**:
    
     * username
     * password
     * remember
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsNotAuthenticated, )
    serializer_class = LoginSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
    def permission_denied(self, request):
        raise exceptions.PermissionDenied(_("You are already authenticated"))


class AccountLogout(APIView):
    """
    Log out
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, format=None):
        """ clear session """
        logout(request)
        return Response({ 'detail': _(u'Logged out successfully') })

class UserRegistrationView(generics.ListCreateAPIView):
    
    """
    Return profile of current authenticated user or return 401.    
    """ 
    
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    model = User
    serializer_class = UserRegistrationSerializer
    
    # custom
    serializer_reader_class = UserProfileSerializer    
    
    def get(self, request, *args, **kwargs):
        """ return profile of current user if authenticated otherwise 401 """
        serializer = self.serializer_reader_class
        
        if request.user.is_authenticated():
            return Response({ 'detail': serializer(request.user, context=self.get_serializer_context()).data })
        else:
            return Response({ 'detail': _('Authentication credentials were not provided') }, status=401)
    
    def post_save(self, obj, created):
        """
        Send email confirmation according to configuration
        """
        super(UserRegistrationView, self).post_save(obj)
        
        if created:
            obj.add_email()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsProfileOwner)
    model = User
    serializer_class = UserProfileSerializer
    lookup_field = 'username'    


class AccountDetail(generics.GenericAPIView):
    """
    Retrieve profile of current user or return 401 if not authenticated.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserProfileSerializer
    
    def get(self, request, format=None):
        """ Retrieve profile of current user or return 401 if not authenticated. """
        serializer = self.serializer_class(request.user, context=self.get_serializer_context())
        return Response(serializer.data)

account_detail = AccountDetail.as_view()

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context