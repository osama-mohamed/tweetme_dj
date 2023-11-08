from rest_framework.serializers import ModelSerializer

from accounts.api.serializers import UserDisplaySerializers
from tweets.models import Tweet


class TweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers()
  class Meta:
    model = Tweet
    fields = [
      'user',
      'content',
      'timestamp',
      'id',
    ]