from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from .models import Tweet

User = get_user_model()


class TweetModelTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username='abc123', password='somepassword')
    Tweet.objects.create(user=user, content='my first tweet')
    Tweet.objects.create(user=user, content='my second tweet')
    Tweet.objects.create(user=user, content='my third tweet')

  def test_tweet_item(self):
    obj = Tweet.objects.create(user=User.objects.first(), content='my fourth tweet')
    self.assertTrue(obj.content == 'my fourth tweet')
    self.assertTrue(obj.id == 4)
    self.assertEqual(obj.id, 4)

  def test_tweet_url(self):
    obj = Tweet.objects.create(user=User.objects.first(), content='my fourth tweet')
    url = reverse('tweets:detail', kwargs={'pk': obj.pk})
    self.assertTrue(obj.get_absolute_url() == url)
  
  def test_tweet_update(self):
    obj = Tweet.objects.create(user=User.objects.first(), content='my fourth tweet')
    content = 'my new tweet'
    obj.content = content
    obj.save()
    self.assertTrue(obj.content == content)

  def test_tweet_delete(self):
    obj = Tweet.objects.create(user=User.objects.first(), content='my fourth tweet')
    self.assertTrue(obj.delete() == (1, {'tweets.Tweet': 1}))
