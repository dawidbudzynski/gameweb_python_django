import random
import unittest

from django.test import TestCase
from django.urls import reverse

from developer.models import Developer
from genre.models import Genre
from tag.models import Tag
from utils.tests import populate_database
from .forms import ChooseTagsForm


class GameRecommendationTests(TestCase, unittest.TestCase):

    def setUp(self):
        populate_database()

    def test_recommendation_manually_content(self):
        response = self.client.get(reverse('game_recommendation:recommend-manually'))
        self.assertEquals(response.status_code, 200)

        form = ChooseTagsForm()
        self.assertFalse(form.is_valid())

        data = {"name": ""}
        form = ChooseTagsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {'developer': ['To pole jest wymagane.'],
             'genre': ['To pole jest wymagane.'],
             'tags': ['To pole jest wymagane.']}
        )

        tag_list = []
        for i in random.sample(range(1, 21), 6):
            tag_list.append(Tag.objects.get(name=f'tag_{i}'))

        data = {
            'developer': Developer.objects.get(name='developer_7').id,
            'genre': Genre.objects.get(name='genre_9').id,
            'tags': tag_list
        }
        form = ChooseTagsForm(data=data)
        self.assertTrue(form.is_valid())
