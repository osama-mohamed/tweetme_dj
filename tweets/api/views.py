from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q


from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination


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
    qs = Tweet.objects.all()
    query = self.request.GET.get('q', None)
    if query is not None:
      qs = qs.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query)
      )
    return qs