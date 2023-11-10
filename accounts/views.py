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
    return context


class UserFollowView(View):
  def get(self, request, username, *args, **kwargs):
    toggle_user = get_object_or_404(User, username__exact=username)
    if request.user.is_authenticated:
      user_profile, created = UserProfile.objects.get_or_create(user=request.user)
      if toggle_user in user_profile.following.all():
        user_profile.following.remove(toggle_user)
      else:
        user_profile.following.add(toggle_user)
    return redirect('accounts:detail', username=username)
