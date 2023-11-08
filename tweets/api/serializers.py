from rest_framework.serializers import ModelSerializer
from django.urls import reverse
from django.utils.timesince import timesince


from accounts.api.serializers import UserDisplaySerializers, SerializerMethodField
from tweets.models import Tweet


class TweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = SerializerMethodField()
  update_url = SerializerMethodField()
  delete_url = SerializerMethodField()
  date_display = SerializerMethodField()
  timesince = SerializerMethodField()

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
    ]

  def get_url(self, obj):
    return self.context.get('request').build_absolute_uri(obj.get_absolute_url())
  
  def get_update_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse('tweets:update', kwargs={'pk': obj.pk}))
  
  def get_delete_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse('tweets:delete', kwargs={'pk': obj.pk}))
  
  def get_date_display(self, obj):
    return obj.timestamp.strftime('%b %d %Y, at %I:%M %p')
  
  def get_timesince(self, obj):
    return timesince(obj.timestamp) + ' ago'