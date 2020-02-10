from importlib import import_module

from django.conf import settings as django_settings
from django.test import RequestFactory, TestCase
from django.shortcuts import reverse

from auth_access import views


class ViewsTestCase(TestCase):

    def test_index(self):
        response = self.client.get(reverse('auth:index'))

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.session['username'] = 'username'
        self.client.session.save()
        response = self.client.get(reverse('auth:logout'), follow=True)

        self.assertNotIn(
            ('username', 'some_user'),
            response.client.session.items())

    def test_redirect(self):
        response = self.client.post(reverse('auth:redirect'),
            {'username': 'some_user'})

        self.assertIn('github', response.url)
