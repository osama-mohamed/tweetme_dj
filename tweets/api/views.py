from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response


from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination



class LikeToggleAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, pk, format=None):
    tweet_qs = Tweet.objects.filter(pk=pk)
    message = 'Not allowed'
    if request.user.is_authenticated:
      is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
      return Response({'liked': is_liked, 'likes': tweet_qs.first().liked.count()})
    return Response({'message': message}, status=400)


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

  def get_serializer_context(self, *args, **kwargs):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context

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


class TweetRetrieveAPIView(ListAPIView):
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]
  # queryset = Tweet.objects.all()
  pagination_class = StandardResultsSetPagination


  def get_queryset(self, *args, **kwargs):
    pk = self.kwargs.get('pk')
    qs = Tweet.objects.filter(pk=pk)
    if qs.exists() and qs.count() == 1:
      parent_obj = qs.first()
      qs1 = parent_obj.get_children()
      qs = (qs | qs1).distinct().extra(select={'parent_id_null': 'parent_id IS NULL'})
    return qs.order_by('-parent_id_null', '-timestamp')

  def get_serializer_context(self, *args, **kwargs):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context

  def retrieve(self, request, *args, **kwargs):
    return Response({'results': self.get_serializer(self.get_object()).data})
  

class SearchTweetAPIView(ListAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]
  pagination_class = StandardResultsSetPagination

  def get_serializer_context(self, *args, **kwargs):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
  
  def get_queryset(self, *args, **kwargs):
    qs = self.queryset
    query = self.request.GET.get('q', None)
    if query is not None:
      qs = qs.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query)
      )
    return qs