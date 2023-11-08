from rest_framework.serializers import ModelSerializer
from django.urls import reverse_lazy, reverse


from accounts.api.serializers import UserDisplaySerializers, SerializerMethodField
from tweets.models import Tweet


class TweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = SerializerMethodField()
  update_url = SerializerMethodField()
  delete_url = SerializerMethodField()

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
    ]

  def get_url(self, obj):
    return self.context.get('request').build_absolute_uri(obj.get_absolute_url())
  
  def get_update_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse('tweets:update', kwargs={'pk': obj.pk}))
  
  def get_delete_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse('tweets:delete', kwargs={'pk': obj.pk}))