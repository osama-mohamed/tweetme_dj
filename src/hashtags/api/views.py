from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from tweets.models import Tweet
from tweets.api.serializers import TweetModelSerializer
from tweets.api.pagination import StandardResultsSetPagination

from hashtags.models import HashTag


class TagTweetAPIView(ListAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]
  pagination_class = StandardResultsSetPagination

  def get_serializer_context(self, *args, **kwargs):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
  
  def get_queryset(self, *args, **kwargs):
    hashtag = self.kwargs.get('hashtag')
    hashtag_obj = None
    try:
      hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]
    except:
      pass
    if hashtag_obj:
      qs = hashtag_obj.get_tweets()
      query = self.request.GET.get('q', None)
      if query is not None:
        qs = qs.filter(
          Q(content__icontains=query) |
          Q(user__username__icontains=query)
        )
      return qs
    return None