from django.urls import path

from .views import (
  TweetListAPIView,
  TweetCreateAPIView,
  RetweetAPIView,
  LikeToggleAPIView,
  TweetRetrieveAPIView,
  SearchTweetAPIView,
)

app_name = 'tweets_api'

urlpatterns = [
  path('', TweetListAPIView.as_view(), name='list'),
  path('search/', SearchTweetAPIView.as_view(), name='search'),
  path('create/', TweetCreateAPIView.as_view(), name='create'),
  path('<int:pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),
  path('<int:pk>/like/', LikeToggleAPIView.as_view(), name='like'),
  path('<int:pk>/', TweetRetrieveAPIView.as_view(), name='detail'),
]