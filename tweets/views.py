from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
  ListView, 
  DetailView,
  CreateView,
)


from .models import Tweet
from .forms import TweetModelForm



class TweetCreateView(CreateView):
  form_class = TweetModelForm
  template_name = 'tweets/create_view.html'
  success_url = reverse_lazy('tweets:list')

  def form_valid(self, form):
    if self.request.user.is_authenticated:
      form.instance.user = self.request.user
      return super().form_valid(form)

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context['title'] = 'Create Tweet'
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