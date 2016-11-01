from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from userena.models import UserenaBaseProfile
from taggit.managers import TaggableManager

# TODO: Let the user have the ability to choose their default language in their profile
# Check http://django-userena.readthedocs.io/en/latest/installation.html#profiles
class UserProfile(UserenaBaseProfile):
    """
        Source: http://django-userena.readthedocs.io/en/latest/installation.html#profiles
    """
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

    @property
    def username(self): 
        """
            Source: http://stackoverflow.com/a/37223506
        """
        return self.user.username


class Queue(models.Model):
    PRIVATE = 'private'
    PUBLIC = 'public'
    PRIVACY_CHOICES = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    )

    owner = models.ForeignKey(UserProfile, related_name='queues')
    name = models.CharField(max_length=30)
    privacy = models.CharField(
        max_length=20,
        choices=PRIVACY_CHOICES,
        default=PRIVATE
    )

    def __str__(self):
        return self.owner.username + '\'s ' + self.name


class MediaService(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Media(models.Model):
    description = models.CharField(max_length=100, default='')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, null=False)

    media_service = models.ForeignKey(MediaService, null=True)
    queue = models.ForeignKey(Queue, related_name='medias')
    tags = TaggableManager()

    @property
    def user(self):
        return self.queue.owner

    def save(self, *args, **kwargs):
        # TODO: auto detect media_service
        if self.media_service is None:  # Set default reference
            self.media_service = MediaService.objects.get(id=1)
        super().save(*args, **kwargs)
