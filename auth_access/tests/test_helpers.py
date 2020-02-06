from django.test import TestCase, Client
from auth_access import helpers

class HelpersTestCase(TestCase):

    def test_get_authorization_url(self):
        params = {
            'client_id': '12345678910',
            'login': 'username',
            'scope': ['write:repo', 'repo']
        }
        auth_url = helpers.generate_url(
                'https://github.com/login/oauth/authorize',
                **params)
        self.assertEqual(auth_url,
            'https://github.com/login/oauth/authorize?client_id=12345678910&login=username&scope=write:repo,repo&')




