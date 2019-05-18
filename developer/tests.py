from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from developer.models import Developer
from .forms import AddDeveloperForm


class DeveloperFormTests(TestCase):

    def test_developer_form(self):
        # redirects to login screen
        response = self.client.get(reverse('developer:developer-create'))
        self.assertEqual('/users/login?next=/pl/developer/developer_create/', response['location'])
        self.assertEquals(response.status_code, 302)

        self.client.force_login(User.objects.get_or_create(username='user_1')[0])
        response = self.client.get(reverse('developer:developer-create'))
        self.assertEquals(response.status_code, 200)

        form = AddDeveloperForm()
        self.assertFalse(form.is_valid())

        data = {"name": ""}
        form = AddDeveloperForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['To pole jest wymagane.']})

        data = {"name": "dev_1"}
        form = AddDeveloperForm(data=data)
        self.assertTrue(form.is_valid())


class DeveloperListTests(TestCase):

    def setUp(self):
        Developer.objects.create(name='developer_1')
        Developer.objects.create(name='developer_2')

    def test_text_content(self):
        dev_object = Developer.objects.get(id=1)
        expected_object_name = f'{dev_object.name}'
        self.assertEquals(expected_object_name, 'developer_1')

    def test_developer_list_view(self):
        response = self.client.get(reverse('developer:developer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'developer_1')
        self.assertEqual(len(response.context[0]['object_list']), 2)
        self.assertTemplateUsed(response, 'developer_list.html')
