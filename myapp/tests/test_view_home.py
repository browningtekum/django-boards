from django.test import TestCase
from django.urls import resolve, reverse

from myapp.views import BoardListView
from myapp.models import Board, Post, Topic


class HomeTests(TestCase):
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_status_code(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)
