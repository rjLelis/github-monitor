from importlib import import_module

from django.conf import settings as django_settings
from django.test import RequestFactory, TestCase
from django.shortcuts import reverse

from auth_access import views


class ViewsTestCase(TestCase):

    def get_session(self):
        if self.client.session:
            session = self.client.session
        else:
            engine = import_module(django_settings.SESSION_ENGINE)
            session = engine.SessionStore()
        return session

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

    def test_get_token(self):
        pass
