from django.db import models
from django.conf import settings
from django.urls import reverse


from .validators import validate_content


class Tweet(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.CharField(max_length=250, validators=[validate_content])
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.content)
  
  def get_absolute_url(self):
    return reverse('tweets:detail', kwargs={'pk': self.pk})