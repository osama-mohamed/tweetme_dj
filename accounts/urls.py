from django.urls import path

from .views import (
  UserDetailView,
)

app_name = 'accounts'

urlpatterns = [
  path('<str:username>/', UserDetailView.as_view(), name='detail'),
]