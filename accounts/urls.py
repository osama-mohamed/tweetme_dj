from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import (
  UserDetailView,
  UserFollowView,
  UserRegisterView,
)

app_name = 'accounts'

urlpatterns = [
  path('', include('django.contrib.auth.urls')),
  path('register/', UserRegisterView.as_view(), name='register'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('<str:username>/follow/', UserFollowView.as_view(), name='follow'),
  path('<str:username>/', UserDetailView.as_view(), name='detail'),
]