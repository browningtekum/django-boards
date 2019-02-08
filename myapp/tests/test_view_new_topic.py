from django.test import TestCase
from django.urls import reverse

from myapp.models import Board


class LoginRequiredNewTopicTests(TestCase):

    # make a request to topic view without being authenticated.
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    # expected result is for the request be redirected to the login view.
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
