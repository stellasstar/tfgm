
# mport from Django
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import *
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.contrib.staticfiles.templatetags.staticfiles import static
import os

@deconstructible
class Avatar_User_Dir(object):
    
    media = settings.MEDIA_ROOT
    av = settings.AVATAR_URL.strip('/')
    def __call__(self, instance, filename):
        joined = os.path.join(self.media,self.av,str(instance.username),filename)
        return joined

avatar_user_dir= Avatar_User_Dir()


class UserManager(BaseUserManager):
    def _create_user(self,
                     username,
                     email=None,
                     password=None,
                     **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username,
                          email=UserManager.normalize_email(email),
                          password=password, created=now,
                          is_admin=False, is_active=True,
                          is_superuser=False,
                          last_login=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    # default profile
    username = models.CharField(_('username'),
                                max_length=30,
                                unique=True,
                                db_index=True)
    email = models.EmailField('email address', unique=True, default="")
    created = models.DateTimeField(_('created'), default=timezone.now)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=True)

    # The additional attributes we wish to include.
    homepage = models.URLField(default="", blank=True)
    picture = models.ImageField(null=True, blank=True,
                                upload_to=avatar_user_dir)
    latitude = models.DecimalField(max_digits=10,
                                   decimal_places=6,
                                   null=True,
                                   default=settings.DEFAULT_LATITUDE)
    longitude = models.DecimalField(max_digits=10,
                                    decimal_places=6,
                                    null=True,
                                    default=settings.DEFAULT_LONGITUDE)

    # user permissions
    is_admin = models.BooleanField(_('admin status'),
                                   default=False,
                                   help_text=_('Designates whether the '
                                               'user can log '
                                               'into this admin site.'))
    is_active = models.BooleanField(_('active'),
                                    default=True,
                                    help_text=_('Designates whether this '
                                                'user should be treated '
                                                'as active. Unselect this '
                                                'instead of deleting '
                                                'accounts.'))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return _("%s's profile") % self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.username])

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name.strip()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
      
    
class PointEntry(geomodels.Model):

    point = geomodels.PointField(srid=4326, blank=True)
    longitude = models.FloatField(verbose_name='longitude')
    latitude = models.FloatField(verbose_name='latitude')    
    
    
    def save(self, *args, **kwargs):
        self.point = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)    
    
    def latitude(self):
        return self.point.y
    
    def longitude(self):
        return self.point.x   