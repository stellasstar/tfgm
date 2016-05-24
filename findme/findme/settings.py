"""
Django settings for googlemaps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django.contrib.auth

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gwn*hqfaxbsrn6mmhzj5$&tndxn(^9q_27pw2*nmbxuw#(_3(!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ADMINS = (
    ('Stella Silverstein', 'stella.silverstein@isotoma.com'),
)
MANAGERS = ADMINS


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'django.contrib.sites',
    'imagekit',
    'crispy_forms',
    'floppyforms',
    'captcha',
    'findme',
    'gatekeeper',
    'transport',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'findme.urls'

WSGI_APPLICATION = 'findme.wsgi.application'

PROJECT_NAME = 'findme'
PROJECT_CORE = 'findme'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geodatabase',
        'USER': 'geouser',
        'PASSWORD': 'geopassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.abspath(BASE_DIR + '/static/'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
AVATAR_ROOT = '/avatars/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"

AVATAR_URL = '/avatars/'
DEFAULT_AVATAR = 'default/woman.jpg'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.static",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.tz",
            ],
        },
    },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_REDIRECT_URL = '/'

# URL of the login page.
LOGIN_URL = 'http://localhost:8000/'

# if user is not logged in then it will redirect the user to login page.
django.contrib.auth.LOGIN_URL = '/'

AUTH_USER_MODEL = 'gatekeeper.UserProfile'
# AUTH_PROFILE_MODULE = 'gatekeeper.UserProfile'

# AUTHENTICATION_BACKENDS = (
#     'django_facebook.auth_backends.FacebookBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )

RECAPTCHA_PUBLIC_KEY = '6LcVu9ESAAAAANVWwbM5-PLuLES94GQ2bIYmSNTG'
RECAPTCHA_PRIVATE_KEY = '6LcVu9ESAAAAAGxz7aEIACWRa3CVnXN3mFd-cajP'

LIST_OF_EMAIL_RECIPIENTS = 'stella.silverstein@isotoma.com'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'testing@example.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_PORT = 1025

# this is in Manchester
DEFAULT_LATITUDE = '53.485900'
DEFAULT_LONGITUDE = '-2.232000'

GOOGLE_API_KEY = 'AIzaSyDxOaCs2l1WYJf4jhNX8AEbTLf2SwncgN4'

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]

IMAGE_MAX_SIZE = 4*1024*1024

AVATAR_DEFAULT_WIDTH = 150
AVATAR_DEFAULT_HEIGHT = 200

handler404 = 'views.handler404'

# when transforming from british nation grid to web mercator standard
# use 2 different coordinate transformation systems for better accuracy
# 27700 -> 4326 -> 3857
# 27700 corresponds to the British National Grid coordinate system
# 4326 corresponds to the U.S. Department of Defense, and is the
#     standard used by the Global Positioning System (GPS)
# 3857 corresponds to Web Mercator and is the standard for Web
#     mapping applications
# bng is the British National Grid
# web_transform is transforming to web standards

US_DOD_GPS = 4326
BRITISH_NATIONAL_GRID = 27700
WEB_MERCATOR_STANDARD = 3857

try:
    from local import *
except ImportError:
    pass