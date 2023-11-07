from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import (
  ListView, 
  DetailView,
  CreateView,
  UpdateView,
  DeleteView,
)

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
  form_class = TweetModelForm
  template_name = 'tweets/create_view.html'
  login_url = '/admin/'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Create Tweet'
    context['btn_title'] = 'Create Tweet'
    return context
  
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    model = Tweet
    fields = ['content']
    template_name = 'tweets/update_view.html'
    login_url = '/admin/'
  
    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      context['title'] = 'Update Tweet'
      context['btn_title'] = 'Update Tweet'
      return context


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy('tweets:list')
    login_url = '/admin/'

    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      context['title'] = 'Delete Tweet'
      return context


class TweetListView(ListView):

  def get_queryset(self, *args, **kwargs):
    qs = Tweet.objects.all()
    query = self.request.GET.get('q', None)
    if query is not None:
      qs = qs.filter(
        Q(content__icontains=query) |
        Q(user__username__icontains=query)
      )
    return qs

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Tweets List'
    context['form'] = TweetModelForm()
    context['btn_title'] = 'New Tweet'
    context['action_url'] = reverse_lazy('tweets:create')
    return context

class TweetDetailView(DetailView):
  queryset = Tweet.objects.all()

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Tweet Detail'
    return context