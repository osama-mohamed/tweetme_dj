from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField


User = get_user_model()

class UserDisplaySerializers(ModelSerializer):
  follower_count = SerializerMethodField()
  url = HyperlinkedIdentityField(
    view_name='accounts:detail',
    lookup_field='username',
  )
  follow_url = HyperlinkedIdentityField(
    view_name='accounts:follow',
    lookup_field='username',
  )
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'last_name',
      'email',
      'id',
      'url',
      'follow_url',
      'follower_count',
    ]

  def get_follower_count(self, obj):
    return obj.followed_by.all().count()