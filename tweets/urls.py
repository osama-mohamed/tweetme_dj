from django.urls import path

from .views import (
  TweetListView,
  TweetDetailView,
  TweetCreateView,
  TweetUpdateView,
)

app_name = 'tweets'

urlpatterns = [
  path('', TweetListView.as_view(), name='list'),
  path('create/', TweetCreateView.as_view(), name='create'),
  path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
  path('<int:pk>/update/', TweetUpdateView.as_view(), name='update'),
]