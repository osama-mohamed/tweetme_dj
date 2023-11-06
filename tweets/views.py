from django.shortcuts import render
from django.views.generic import ListView, DetailView


from .models import Tweet


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