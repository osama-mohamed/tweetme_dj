from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
import re


from hashtags.signals import parsed_hashtags
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
      reply=False,
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
  
  def like_toggle(self, user, tweet_obj):
    if user in tweet_obj.liked.all():
      is_liked = False
      tweet_obj.liked.remove(user)
    else:
      is_liked = True
      tweet_obj.liked.add(user)
    return is_liked


class Tweet(models.Model):
  parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.CharField(max_length=250, validators=[validate_content])
  liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
  reply = models.BooleanField(verbose_name='Is a reply?', default=False)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  objects = TweetManager()

  class Meta:
    ordering = ['-timestamp']

  def __str__(self):
    return str(self.content)
  
  def get_absolute_url(self):
    return reverse('tweets:detail', kwargs={'pk': self.pk})
  
  def get_parent(self):
    the_parent = self
    if self.parent:
      the_parent = self.parent
    return the_parent
  
  def get_children(self):
    parent = self.get_parent()
    qs = Tweet.objects.filter(parent=parent)
    qs_parent = Tweet.objects.filter(pk=parent.pk)
    return (qs | qs_parent)


def tweet_post_save_receiver(sender, instance, created, *args, **kwargs):
  if created and not instance.parent:
    user_regex = r'@(?P<username>[\w.@+-]+)'
    user_matches = re.findall(user_regex, instance.content)
    for username in user_matches:
      print(username) # send notification to user here.
    hashtag_regex = r'#(?P<hashtag>[\w\d-]+)'
    hashtag_matches = re.findall(hashtag_regex, instance.content)
    parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtag_matches)
    for hashtag in hashtag_matches:
      print(hashtag) # send hashtag signal to user here.


post_save.connect(tweet_post_save_receiver, sender=Tweet)