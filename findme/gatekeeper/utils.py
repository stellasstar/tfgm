import os
import StringIO
import urllib2
from urlparse import urlparse
from django.core.files.base import ContentFile
import httplib
from django.conf import settings
from gatekeeper import models

# image processing
from PIL import Image
from django.core.files.storage import default_storage

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


def image_exists(domain, path):
    # http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists
    try:
        conn = httplib.HTTPConnection(domain)
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
    except:
        return False
    return response.status == 200


def get_extension(filename):
    return os.path.splitext(filename)[1]


def get_url_tail(url):
    return url.split('/')[-1]


def make_thumbnail(image, name, ext):
    """
    Create and save the thumbnail for the photo (simple resize with PIL).
    """
    try:
        image = Image.open(User.thumbnail)
        sett = (settings.AVATAR_DEFAULT_HEIGHT, settings.AVATAR_DEFAULT_WIDTH)
        image.thumbnail(sett)
    except IOError:
        return False

    thumb_buffer = StringIO.StringIO()

    image.save(thumb_buffer, format=image.format)
    thumb_name, thumb_extension = (name.lower(), ext.lower())
    thumb = models.Avatar_User_Dir(thumb_name + '_thumb' + thumb_extension)

    s3_thumb = default_storage.open(thumb, 'w')
    s3_thumb.write(thumb_buffer.getvalue())
    s3_thumb.close()

    return True


def pil_to_django(image, format="JPEG"):
    fobject = StringIO.StringIO()
    image.save(fobject, format=format)
    return ContentFile(fobject.getvalue())


def retrieve_image(url):
    return StringIO.StringIO(urllib2.urlopen(url).read())


def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path


def valid_image_size(image):
    max_size = settings.IMAGE_MAX_SIZE
    width, height = image.size
    if (width * height) > max_size:
        return (False, "Image is too large")
    return (True, image)


def valid_url_extension(url):
    extension_list = settings.VALID_IMAGE_EXTENSIONS
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list])
