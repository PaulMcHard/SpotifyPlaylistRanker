from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import os

class HomePageTest(TestCase):

    def test_index_load(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_rankings_load(self):
        response = self.client.get(reverse('rankings'))
        self.assertEqual(response.status_code, 200)
