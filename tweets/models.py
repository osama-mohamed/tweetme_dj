from django.db import models
from django.conf import settings
from django.urls import reverse
from  django.utils import timezone


from .validators import validate_content


class TweetManager(models.Manager):
  def retweet(self, user, parent_obj):
    if parent_obj.parent:
      og_parent = parent_obj.parent
    else:
      og_parent = parent_obj
    qs = self.get_queryset().filter(user=user, parent=og_parent).filter(
      timestamp__year=timezone.now().year,
      timestamp__month=timezone.now().month,
      timestamp__day=timezone.now().day,
    )
    if qs.exists():
      return None
    obj = self.model(
      parent=og_parent,
      user=user,
      content=parent_obj.content
    )
    obj.save()
    return obj

class Tweet(models.Model):
  parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.CharField(max_length=250, validators=[validate_content])
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = TweetManager()

  class Meta:
    ordering = ['-timestamp']

  def __str__(self):
    return str(self.content)
  
  def get_absolute_url(self):
    return reverse('tweets:detail', kwargs={'pk': self.pk})