from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from genre.models import Genre
from .forms import AddGenreForm


class GenreFormTests(TestCase):

    def test_genre_form(self):
        # redirects to login screen
        response = self.client.get(reverse('genre:genre-create'))
        self.assertEqual('/users/login?next=/pl/genre/genre_create/', response['location'])
        self.assertEquals(response.status_code, 302)

        self.client.force_login(User.objects.get_or_create(username='user_1')[0])
        response = self.client.get(reverse('genre:genre-create'))
        self.assertEquals(response.status_code, 200)

        form = AddGenreForm()
        self.assertFalse(form.is_valid())

        data = {"name": ""}
        form = AddGenreForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['To pole jest wymagane.']})

        data = {"name": "genre_1"}
        form = AddGenreForm(data=data)
        self.assertTrue(form.is_valid())


class GenreListTests(TestCase):

    def setUp(self):
        Genre.objects.create(name='genre_1')
        Genre.objects.create(name='genre_2')

    def test_text_content(self):
        genre_object = Genre.objects.get(name='genre_1')
        expected_object_name = f'{genre_object.name}'
        self.assertEquals(expected_object_name, 'genre_1')

    def test_genre_list_view(self):
        response = self.client.get(reverse('genre:genre-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'genre_1')
        self.assertEqual(len(response.context[0]['object_list']), 2)
        self.assertTemplateUsed(response, 'genre_list.html')
