from django.db import utils as db_utils
from github import Github
from github.GithubException import UnknownObjectException

from rest_framework import status

from .models import Profile, Repository, Commit


def create_profile(**kwargs):
    try:
        username = kwargs.pop('username')
        profile, created = Profile.objects.get_or_create(
            username=username, defaults=kwargs)
        if not created:
            profile.name = kwargs.get('name', profile.name)
            profile.email = kwargs.get('email', profile.email)
            profile.access_token = kwargs.get('access_token',
                                              profile.access_token)
            profile.save()

        return profile, created
    except db_utils.IntegrityError:
        raise (f'username can\'t be null', status.HTTP_400_BAD_REQUEST)


def get_profile(**login_or_token):
    try:
        profile = Profile.objects.get(**login_or_token)
        return profile, status.HTTP_200_OK
    except Profile.DoesNotExist:
        raise Exception('User not found', status.HTTP_404_NOT_FOUND)


def get_repositories_by_user(username):
    repos = Repository.objects.filter(owner__username=username).all()
    return repos


def create_repository(profile, full_name_or_id):
    try:
        g = Github(profile.access_token)
        repo = g.get_repo(full_name_or_id=full_name_or_id)
        new_repository = Repository.objects.create(
            name=repo.name,
            description=repo.description,
            owner=profile,
        )

        create_commits(repo, new_repository)
        create_hook(repo)

        return new_repository

    except db_utils.IntegrityError:
        raise Exception('repo already on the list',
                        status.HTTP_400_BAD_REQUEST)
    except UnknownObjectException:
        raise Exception('repo not found', status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise e.args


def create_commits(github_repo, repo_object):
    # Todo: add query to get commits only from the last month
    try:
        commits = github_repo.get_commits()
        commit_list = []
        for commit in commits:
            profile, _ = create_profile(
                name=commit.author.name,
                username=commit.author.login,
                email=commit.author.email
            )

            new_commit = Commit(
                sha=commit.sha,
                commiter=profile,
                commited_at=commit.commit.committer.date,
                message=commit.commit.message,
                repository=repo_object
            )

            commit_list.append(new_commit)

        Commit.objects.bulk_create(commit_list)
    except db_utils.IntegrityError:
        raise Exception('commit already on the list',
                        status.HTTP_400_BAD_REQUEST)


def get_commits_by_repo(repo_full_name):
    commits = Commit.objects.filter(
        repository__full_name=repo_full_name
    ).all().order_by('-commited_at')

    return commits


def create_hook(repo):
    # Todo: Adicionar reverse na config['url']
    # Todo: Adicionar try..except para tratar o retorno
    config = {
        'url': 'http://localhost:8000/api/repositories',
        'content_type': 'json'
    }
    events = ['push']
    repo.create_hook('monitor', config, envents, active=True)
