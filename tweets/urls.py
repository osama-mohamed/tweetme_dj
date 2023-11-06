from django.urls import path

from .views import (
  tweet_list_view,
  tweet_detail_view,
)

app_name = 'tweets'

urlpatterns = [
  path('', tweet_list_view, name='list'),
  path('<int:pk>/', tweet_detail_view, name='detail'),
]