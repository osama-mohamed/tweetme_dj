from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()

class UserDisplaySerializers(ModelSerializer):
  follower_count = SerializerMethodField()
  url = SerializerMethodField()
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'last_name',
      'email',
      'id',
      'url',
      'follower_count',
    ]

  def get_url(self, obj):
    return self.context.get('request').build_absolute_uri(reverse_lazy('accounts:detail', kwargs={'username': obj.username}))
  
  def get_follower_count(self, obj):
    return 0