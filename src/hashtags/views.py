from multiprocessing import context
from django.shortcuts import render
from django.views.generic import View


from .models import HashTag


class HashTagView(View):
  def get(self, request, hashtag, *args, **kwargs):
    obj, created = HashTag.objects.get_or_create(tag=hashtag)
    context = {
      'obj': obj,
      'title': 'Hashtag',
      }
    return render(request, 'hashtags/tag_view.html', context)
