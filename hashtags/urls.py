from django.urls import path

from .views import HashTagView

app_name = 'hashtags'

urlpatterns = [
  path('<str:hashtag>/', HashTagView.as_view(), name='detail'),
]