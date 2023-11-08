from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from tweets.models import Tweet
from .serializers import TweetModelSerializer


class TweetListAPIView(ListAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]