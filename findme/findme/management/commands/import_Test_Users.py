import os
import findme

from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.core.management.base import BaseCommand

from transport.models import Position

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class Command(BaseCommand):
    help = 'create test Users'

    def handle(self, *args, **options):
        User.objects.all().delete()
        user = User.objects.create_user(
                   username = 'testCommenter',
                   email = 'testCommenter@test.com',
                   password = 'test',
               )
        user.first_name = 'test'
        user.last_name = 'commenter'
        user.set_password('test')
        lat = settings.DEFAULT_LATITUDE
        lng = settings.DEFAULT_LONGITUDE
        lString = 'POINT(%s %s)' % (lng, lat)
        new_position = Position(
            user=user,
            name=user.username,
            geometry=fromstr(lString))
        user.save()
        new_position.save()
        user.position = new_position
        user.save()
        new_position.user = user
        new_position.save()
        
        user2 = User.objects.create_user(username = 'stella',
                    email = 'stella.silverstein@isotoma.com',
                    password = 'stella',)
        user2.first_name = 'stella'
        user2.last_name = 'silverstein'
        user.set_password('stella')
        new_position = Position(
                    user=user2,
                    name=user2.username,
                    geometry=fromstr(lString))
        user2.save()
        new_position.save()
        user2.position = new_position
        user2.save()
        new_position.user = user2
        new_position.save()
