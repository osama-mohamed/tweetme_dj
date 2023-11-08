from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()

class UserDisplaySerializers(ModelSerializer):
  follower_count = SerializerMethodField()
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'last_name',
      'email',
      'id',
      'follower_count',
    ]

  def get_follower_count(self, obj):
    return 0