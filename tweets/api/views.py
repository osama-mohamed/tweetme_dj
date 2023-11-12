from multiprocessing import context
from urllib import request
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response


from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination



class RetweetAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, pk, format=None):
    tweet_qs = Tweet.objects.filter(pk=pk)
    message = 'Not allowed'
    if tweet_qs.exists() and tweet_qs.count() == 1:
      if request.user.is_authenticated:
        new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
        if new_tweet is not None:
          data = TweetModelSerializer(new_tweet, context={'request': self.request}).data
          return Response(data)
        message = 'Cannot retweet the same in 1 day'
    return Response({'message': message}, status=400)


class TweetCreateAPIView(CreateAPIView):
  serializer_class = TweetModelSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class TweetListAPIView(ListAPIView):
  # queryset = Tweet.objects.all()
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]
  pagination_class = StandardResultsSetPagination

  def get_queryset(self, *args, **kwargs):
    requested_user = self.kwargs.get('username')
    if requested_user:
      qs = Tweet.objects.filter(user__username=requested_user)
    else:
      im_following = self.request.user.profile.get_following()
      qs1 = Tweet.objects.filter(user__in=im_following)
      qs2 = Tweet.objects.filter(user=self.request.user)
      qs = (qs1 | qs2).distinct()
    query = self.request.GET.get('q', None)
    if query is not None:
      qs = qs.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query)
      )
    return qs