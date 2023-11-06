from django.urls import path

from .views import (
  TweetListView,
  TweetDetailView,
)

app_name = 'tweets'

urlpatterns = [
  path('', TweetListView.as_view(), name='list'),
  path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
]