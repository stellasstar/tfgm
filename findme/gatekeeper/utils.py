import os
import StringIO
import urllib2
from urlparse import urlparse
from django.core.files.base import ContentFile
import httplib
from django.conf import settings

def valid_image_size(image):
    max_size=settings.IMAGE_MAX_SIZE
    width, height = image.size
    if (width * height) > max_size:
        return (False, "Image is too large")
    return (True, image)

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

def retrieve_image(url):
    return StringIO.StringIO(urllib2.urlopen(url).read())

def valid_url_extension(url):
    extension_list=settings.VALID_IMAGE_EXTENSIONS
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list]) 

def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path

def get_url_tail(url):
    return url.split('/')[-1]  

def get_extension(filename):
    return os.path.splitext(filename)[1]

def pil_to_django(image, format="JPEG"):
    # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
    fobject = StringIO.StringIO()
    image.save(fobject, format=format)
    return ContentFile(fobject.getvalue())