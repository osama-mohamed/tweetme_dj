from django.urls import path

from .views import (
  TweetListView,
  TweetDetailView,
  TweetCreateView,
)

app_name = 'tweets'

urlpatterns = [
  path('', TweetListView.as_view(), name='list'),
  path('create/', TweetCreateView.as_view(), name='create'),
  path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
]