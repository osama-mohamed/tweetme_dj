from django.urls import path

from .views import (
  TweetListAPIView,
)

app_name = 'tweets_api'

urlpatterns = [
  path('', TweetListAPIView.as_view(), name='list'),
]