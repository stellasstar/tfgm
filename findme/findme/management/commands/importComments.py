import os
import findme

from django.core.management.base import BaseCommand

from transport.models import Waypoint, Comment

class Command(BaseCommand):
    help = 'Loads Tfgm geospatial data from app data directory'
    comments = 'static/data/comments.csv'

    def handle(self, *args, **options):
        comments_file = os.path.abspath(os.path.join(os.path.join(
            os.path.dirname(findme.__file__), self.comments)))
        f = open(comments_file, 'r')
        for line in f:
            words = line.split(",")
            way=words[0].strip()
            print way
            w = Waypoint.objects.get(id=way)
            comment = Comment.objects.create()
            comment.post = w
            comment.author = "testCommenter"
            comment.text = words[1]
            comment.approved_comment = True
            print w
            comment.save()