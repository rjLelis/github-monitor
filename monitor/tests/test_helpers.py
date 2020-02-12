from django.test import TestCase
from monitor import helpers
from monitor.models import Profile, Repository

class HelpersTestCase(TestCase):

    def setUp(self):
        profile = Profile.objects.create(
            username='rjLelis',
            name='some user',
            email='someUser@test.com',
            access_token='718fab2a729bdee9d001fdb923277a0b39ae9e60'
        )

        for i in range(5):
            Repository.objects.create(
                name=f'repo{i}',
                owner=profile
            )

    def test_create_profile(self):
        new_profile = {
            'username': 'new_user',
            'name': 'A name',
            'email': 'new_user@test.com',
        }
        profile = helpers.create_profile(**new_profile)

        self.assertIsNotNone(profile)

    def test_update_acess_token_profile(self):
        profile = {
            'username': 'rjLelis',
            'email': 'newUseremail@test.com.br'
        }

        profile = helpers.create_profile(**profile)

        self.assertEquals(profile.email, 'newUseremail@test.com.br')

    def test_get_profile(self):

        profile = helpers.get_profile(username='rjLelis')

        self.assertIsNotNone(profile)

    def test_get_repositories_by_user(self):
        repositories = helpers.get_repositories_by_user('rjLelis')

        self.assertEquals(len(repositories), 5)


    def test_empty_repository_list(self):
        repositories = helpers.get_repositories_by_user('user')

        self.assertEquals(len(repositories), 0)

    def test_get_repository_by_full_name(self):
        repo = helpers.get_repository_by_full_name('rjLelis/repo1')

        self.assertIsNotNone(repo)

    def test_create_repository(self):
        # Obs: tested with real Github user and repo
        profile = helpers.get_profile(username='rjLelis')
        repo = helpers.create_repository(profile, 'rjLelis/todo-app')

        self.assertEquals(
            repo.description,
            'A todo app made with Django rest framework and Reactjs'
        )
