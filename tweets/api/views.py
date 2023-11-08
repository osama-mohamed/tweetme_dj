from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q


from tweets.models import Tweet
from .serializers import TweetModelSerializer


class TweetListAPIView(ListAPIView):
  # queryset = Tweet.objects.all()
  serializer_class = TweetModelSerializer
  permission_classes = [AllowAny]

  def get_queryset(self, *args, **kwargs):
    qs = Tweet.objects.all()
    query = self.request.GET.get('q', None)
    if query is not None:
      qs = qs.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query)
      )
    return qs