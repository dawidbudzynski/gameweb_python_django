import unittest

from django.test import TestCase
from django.urls import reverse


class NewsAPITests(TestCase, unittest.TestCase):

    def test_game_form(self):
        response = self.client.get(reverse('news_api:show-news', kwargs={'news_source': 'polygon'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_main.html')
