import unittest

from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase
from django.urls import reverse

from developer.models import Developer
from game.models import Game
from genre.models import Genre
from tag.models import Tag
from users.models import User
from .forms import AddGameForm


class GameFormTests(TestCase, unittest.TestCase):

    def setUp(self):
        django_user = DjangoUser.objects.create(
            username='user_1',
            password='password_1',
            first_name='first_name_1',
            last_name='last_name_1',
            email='email_1'
        )
        self.user = User.objects.create(user=django_user)

        Genre.objects.create(name='genre_1')
        Developer.objects.create(name='developer_1')
        for i in range(1, 7):
            Tag.objects.create(name=f'tag_{i}')

        game_1 = Game.objects.create(
            developer=Developer.objects.get(name='developer_1'),
            genre=Genre.objects.get(name='genre_1'),
            title='game_1',
            year=2015,
            to_be_rated=False
        )
        for tag in Tag.objects.all():
            game_1.tags.add(tag)
        game_1.save()

    def test_game_form(self):
        # redirects to login screen
        response = self.client.get(reverse('game:game-create'))
        self.assertEqual('/users/login?next=/pl/game/game_create/', response['location'])
        self.assertEquals(response.status_code, 302)

        self.client.force_login(DjangoUser.objects.get_or_create(username='user_1')[0])
        response = self.client.get(reverse('game:game-create'))
        self.assertEquals(response.status_code, 200)

        form = AddGameForm()
        self.assertFalse(form.is_valid())

        data = {"name": ""}
        form = AddGameForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'developer': ['To pole jest wymagane.'],
            'genre': ['To pole jest wymagane.'],
            'tags': ['To pole jest wymagane.'],
            'title': ['To pole jest wymagane.'],
            'year': ['To pole jest wymagane.']
        })

        data = {
            'developer': Developer.objects.get(name='developer_1').id,
            'genre': Genre.objects.get(name='genre_1').id,
            'tags': [
                Tag.objects.get(name='tag_1'),
                Tag.objects.get(name='tag_2'),
                Tag.objects.get(name='tag_3'),
                Tag.objects.get(name='tag_4'),
                Tag.objects.get(name='tag_5'),
                Tag.objects.get(name='tag_6')
            ],
            'title': 'game_1',
            'year': 2015,
            'to_be_rated': False
        }
        form = AddGameForm(data=data)
        self.assertTrue(form.is_valid())

    def test_created_object(self):
        game_object = Game.objects.get(title='game_1')
        developer_id = 1 if settings.WORK_ON_SQL_LITE else 5
        self.assertDictContainsSubset({
            'developer_id': developer_id,
            'genre_id': 1,
            'id': 1,
            'image': '',
            'title': 'game_1',
            'to_be_rated': False,
            'year': 2015},
            game_object.__dict__
        )

    def test_game_list_view(self):
        response = self.client.get(reverse('game:game-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'game_1')
        self.assertEqual(len(response.context[0]['object_list']), 1)
        self.assertTemplateUsed(response, 'game_list.html')
