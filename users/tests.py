from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase
from django.urls import reverse

from users.models import User
from .forms import AddUserForm


class UserFormTests(TestCase):

    def test_user_form(self):
        response = self.client.get(reverse('users:user-create'))
        self.assertEquals(response.status_code, 200)

        self.client.force_login(DjangoUser.objects.get_or_create(username='user_1', is_superuser=True)[0])
        response = self.client.get(reverse('users:user-create'))
        self.assertEquals(response.status_code, 200)

        form = AddUserForm()
        self.assertFalse(form.is_valid())

        data = {"name": "", 'password': ''}
        form = AddUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['To pole jest wymagane.'],
            'password': ['To pole jest wymagane.']
        })

        data = {"username": "user_1", 'password': 'password_1'}
        form = AddUserForm(data=data)
        self.assertTrue(form.is_valid())


class UserViewsTests(TestCase):

    def setUp(self):
        django_user = DjangoUser.objects.create(
            username='user_1',
            password='password_1',
            first_name='first_name_1',
            last_name='last_name_1',
            email='email_1'
        )
        User.objects.create(user=django_user)
