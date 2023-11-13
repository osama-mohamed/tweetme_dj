from multiprocessing import context
from rest_framework.serializers import ModelSerializer
from django.urls import reverse_lazy
from django.utils.timesince import timesince


from accounts.api.serializers import UserDisplaySerializers, SerializerMethodField
from tweets.models import Tweet


class ParentTweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = SerializerMethodField()
  update_url = SerializerMethodField()
  delete_url = SerializerMethodField()
  date_display = SerializerMethodField()
  timesince = SerializerMethodField()
  retweet_url = SerializerMethodField()
  like_url = SerializerMethodField()

  class Meta:
    model = Tweet
    fields = [
      'user',
      'id',
      'content',
      'timestamp',
      'url',
      'update_url',
      'delete_url',
      'date_display',
      'timesince',
      'retweet_url',
      'like_url',
    ]

  def get_url(self, obj):
    return self.context.get('request').build_absolute_uri(obj.get_absolute_url())
  
  def get_update_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets:update', kwargs={'pk': obj.pk}))
  
  def get_delete_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets:delete', kwargs={'pk': obj.pk}))
  
  def get_date_display(self, obj):
    return obj.timestamp.strftime('%b %d %Y, at %I:%M %p')
  
  def get_timesince(self, obj):
    return timesince(obj.timestamp) + ' ago'
  
  def get_retweet_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets_api:retweet', kwargs={'pk': obj.pk}))
  
  def get_like_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets_api:like', kwargs={'pk': obj.pk}))



class TweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = SerializerMethodField()
  update_url = SerializerMethodField()
  delete_url = SerializerMethodField()
  date_display = SerializerMethodField()
  timesince = SerializerMethodField()
  retweet_url = SerializerMethodField()
  like_url = SerializerMethodField()
  parent = ParentTweetModelSerializer(read_only=True)

  class Meta:
    model = Tweet
    fields = [
      'user',
      'id',
      'content',
      'timestamp',
      'url',
      'update_url',
      'delete_url',
      'date_display',
      'timesince',
      'retweet_url',
      'like_url',
      'parent',
    ]

  def get_url(self, obj):
    return self.context.get('request').build_absolute_uri(obj.get_absolute_url())
  
  def get_update_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets:update', kwargs={'pk': obj.pk}))
  
  def get_delete_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets:delete', kwargs={'pk': obj.pk}))
  
  def get_date_display(self, obj):
    return obj.timestamp.strftime('%b %d %Y, at %I:%M %p')
  
  def get_timesince(self, obj):
    return timesince(obj.timestamp) + ' ago'
  
  def get_retweet_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets_api:retweet', kwargs={'pk': obj.pk}))
  
  def get_like_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('tweets_api:like', kwargs={'pk': obj.pk}))