from django.urls import path

from .views import (
  TweetListView,
  TweetDetailView,
  TweetCreateView,
  TweetUpdateView,
  TweetDeleteView,
  RetweetView,
  SearchView,
)

app_name = 'tweets'

urlpatterns = [
  path('', TweetListView.as_view(), name='list'),
  path('search/', SearchView.as_view(), name='search'),
  path('create/', TweetCreateView.as_view(), name='create'),
  path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
  path('<int:pk>/retweet/', RetweetView.as_view(), name='retweet'),
  path('<int:pk>/update/', TweetUpdateView.as_view(), name='update'),
  path('<int:pk>/delete/', TweetDeleteView.as_view(), name='delete'),
]