import os, sys, time
from random import randint
import findme

from django.contrib.auth import authenticate, login, logout
from django.core.management.base import BaseCommand
from django.utils import timezone

from transport.models import Waypoint, Comment

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class Command(BaseCommand):
    help = 'Loads Tfgm geospatial data from app data directory'
    comments = 'static/data/comments.csv'

    def handle(self, *args, **options):
        # Comment.objects.all().delete()
        comments_file = os.path.abspath(os.path.join(os.path.join(
            os.path.dirname(findme.__file__), self.comments)))
        with open(comments_file) as f:
            lines = f.read().splitlines()
        ways = Waypoint.objects.all()
        user = User.objects.get(username = 'testCommenter')
        for way in ways:
            comment = Comment.objects.create(author = user)
            comment.comment = lines[randint(0,2)]
            comment.waypoint = way
            comment.approved_comment = True
            #way.comments.create(comment)
            comment.save()
            #way.save()
            print str(way.id), way
