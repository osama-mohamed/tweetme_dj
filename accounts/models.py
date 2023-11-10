from django.conf import settings
from django.db import models


class UserProfileManager(models.Manager):
  use_for_related_fields = True

  def all(self):
    qs = self.get_queryset().all()
    try:
      if self.instance:
        qs = qs.exclude(user=self.instance)
    except:
      pass
    return qs


class UserProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE) # user.profile
  following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by', blank=True)
  # user.profile.following -- users I follow
  # user.followed_by -- users that follow me - reverse relationship

  objects = UserProfileManager()

  def __str__(self):
    return str(self.following.all().count())
  
  def get_following(self):
    users = self.following.all()
    return users.exclude(username=self.user.username)
