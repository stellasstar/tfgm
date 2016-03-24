
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from awesome_avatar.fields import AvatarField
from django.conf import settings

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, unique=True, verbose_name='user')
    
     # The additional attributes we wish to include.
    homepage = models.URLField(default='http://www.none.com', blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to=settings.AVATAR_URL)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default='53.483959')
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, default='-2.244644')
    

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username  
    
    def user_post_save(sender, instance, created, **kwargs):
        profile, new = UserProfile.objects.get_or_create(user=instance)
    
    models.signals.post_save.connect(user_post_save, User)
