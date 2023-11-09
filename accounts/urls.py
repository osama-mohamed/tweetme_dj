from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
  UserDetailView,
)

app_name = 'accounts'

urlpatterns = [
  path('logout/', LogoutView.as_view(), name='logout'),
  path('<str:username>/', UserDetailView.as_view(), name='detail'),
]