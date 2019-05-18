from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tag.models import Tag
from .forms import AddTagForm


class TagFormTests(TestCase):

    def test_genre_form(self):
        # redirects to login screen
        response = self.client.get(reverse('tag:tag-create'))
        self.assertEqual('/users/login?next=/pl/tag/tag_create/', response['location'])
        self.assertEquals(response.status_code, 302)

        self.client.force_login(User.objects.get_or_create(username='user_1')[0])
        response = self.client.get(reverse('tag:tag-create'))
        self.assertEquals(response.status_code, 200)

        form = AddTagForm()
        self.assertFalse(form.is_valid())

        data = {"name": ""}
        form = AddTagForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['To pole jest wymagane.']})

        data = {"name": "tag_1"}
        form = AddTagForm(data=data)
        self.assertTrue(form.is_valid())


class TagListTests(TestCase):

    def setUp(self):
        Tag.objects.create(name='tag_1')
        Tag.objects.create(name='tag_2')

    def test_text_content(self):
        tag_object = Tag.objects.get(id=1)
        expected_object_name = f'{tag_object.name}'
        self.assertEquals(expected_object_name, 'tag_1')

    def test_tag_list(self):
        response = self.client.get(reverse('tag:tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tag_1')
        self.assertEqual(len(response.context[0]['object_list']), 2)
        self.assertTemplateUsed(response, 'tag_list.html')
