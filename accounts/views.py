from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import DetailView

from .models import UserProfile


User = get_user_model()


class UserDetailView(DetailView):
  queryset = User.objects.all()
  template_name = 'accounts/user_detail.html'

  def get_object(self):
    return get_object_or_404(User, username__iexact=self.kwargs.get('username'))

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'User Detail'
    context['following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
    return context


class UserFollowView(View):
  def get(self, request, username, *args, **kwargs):
    toggle_user = get_object_or_404(User, username__exact=username)
    if request.user.is_authenticated:
      is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
    return redirect('accounts:detail', username=username)
