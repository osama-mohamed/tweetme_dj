from multiprocessing import context
from django.shortcuts import render

from .models import Tweet


def tweet_list_view(request):
  qs = Tweet.objects.all()
  context = {
    'object_list': qs,
    'title': 'List',
  }
  return render(request, 'tweets/list.html', context)


def tweet_detail_view(request, pk=1):
  obj = Tweet.objects.get(pk=pk)
  context = {
    'object': obj,
    'title': 'Detail',
  }
  return render(request, 'tweets/detail.html', context)