from rest_framework.serializers import ModelSerializer, CharField, HyperlinkedIdentityField
from django.utils.timesince import timesince


from accounts.api.serializers import UserDisplaySerializers, SerializerMethodField
from tweets.models import Tweet


class ParentTweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = HyperlinkedIdentityField(
    view_name='tweets:detail',
  )
  update_url = HyperlinkedIdentityField(
    view_name='tweets:update',
  )
  delete_url = HyperlinkedIdentityField(
    view_name='tweets:delete',
  )
  date_display = SerializerMethodField()
  timesince = SerializerMethodField()
  retweet_url = HyperlinkedIdentityField(
    view_name='tweets_api:retweet',
  )
  like_url = HyperlinkedIdentityField(
    view_name='tweets_api:like',
  )
  likes = SerializerMethodField()
  did_like = SerializerMethodField()

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
      'likes',
      'did_like',
    ]

  def get_date_display(self, obj):
    return obj.timestamp.strftime('%b %d %Y, at %I:%M %p')
  
  def get_timesince(self, obj):
    return timesince(obj.timestamp) + ' ago'

  def get_likes(self, obj):
    return obj.liked.all().count()

  def get_did_like(self, obj):
    request = self.context.get('request')
    user = request.user
    if user.is_authenticated:
      if user in obj.liked.all():
        return True
    return False



class TweetModelSerializer(ModelSerializer):
  user = UserDisplaySerializers(read_only=True)
  url = HyperlinkedIdentityField(
    view_name='tweets:detail',
  )
  update_url = HyperlinkedIdentityField(
    view_name='tweets:update',
  )
  delete_url = HyperlinkedIdentityField(
    view_name='tweets:delete',
  )
  date_display = SerializerMethodField()
  timesince = SerializerMethodField()
  retweet_url = HyperlinkedIdentityField(
    view_name='tweets_api:retweet',
  )
  like_url = HyperlinkedIdentityField(
    view_name='tweets_api:like',
  )

  likes = SerializerMethodField()
  did_like = SerializerMethodField()
  parent = ParentTweetModelSerializer(read_only=True)
  parent_id = CharField(write_only=True, required=False)
  owner = SerializerMethodField()

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
      'likes',
      'did_like',
      'parent',
      'reply',
      'parent_id',
      'owner',
    ]

    # read_only_fields = ['reply']
  
  def get_date_display(self, obj):
    return obj.timestamp.strftime('%b %d %Y, at %I:%M %p')
  
  def get_timesince(self, obj):
    return timesince(obj.timestamp) + ' ago'

  def get_likes(self, obj):
    return obj.liked.all().count()
  
  def get_did_like(self, obj):
    request = self.context.get('request')
    user = request.user
    if user.is_authenticated:
      if user in obj.liked.all():
        return True
    return False
  
  def get_owner(self, obj):
    tweet_owner = obj.user.username
    current_user = self.context.get('request').user.username
    if tweet_owner == current_user:
      return True, tweet_owner
    return False, tweet_owner