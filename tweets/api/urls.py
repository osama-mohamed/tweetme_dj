from django.urls import path

from .views import (
  TweetListAPIView,
  TweetCreateAPIView,
  RetweetAPIView,
)

app_name = 'tweets_api'

urlpatterns = [
  path('', TweetListAPIView.as_view(), name='list'),
  path('create/', TweetCreateAPIView.as_view(), name='create'),
  path('<int:pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),
]