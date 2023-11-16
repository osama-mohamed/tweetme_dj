from django.urls import path

from .views import (
  TagTweetAPIView,
)

app_name = 'tags_api'

urlpatterns = [
  path('<str:hashtag>/', TagTweetAPIView.as_view(), name='list'),
]