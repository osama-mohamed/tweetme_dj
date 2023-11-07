from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
  ListView, 
  DetailView,
  CreateView,
  UpdateView,
)

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
  form_class = TweetModelForm
  template_name = 'tweets/create_view.html'
  success_url = reverse_lazy('tweets:list')
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
    success_url = reverse_lazy('tweets:list')
    login_url = '/admin/'
  
    def get_context_data(self, *args, **kwargs):
      context = super().get_context_data(*args, **kwargs)
      context['title'] = 'Update Tweet'
      context['btn_title'] = 'Update Tweet'
      return context


class TweetListView(ListView):
  queryset = Tweet.objects.all()

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Tweets List'
    return context

class TweetDetailView(DetailView):
  queryset = Tweet.objects.all()

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Tweet Detail'
    return context