from django.db import utils as db_utils
from django.urls import reverse
from github import Github
from github.GithubException import GithubException, UnknownObjectException
from rest_framework import status
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination

from .models import Commit, Profile, Repository


def create_profile(**new_profile):
    try:
        username = new_profile.pop('username')
        profile, created = Profile.objects.get_or_create(
            username=username, defaults=new_profile)
        if not created:
            profile.name = new_profile.get('name', profile.name)
            profile.email = new_profile.get('email', profile.email)
            profile.access_token = new_profile.get('access_token',
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
    repos = Repository.objects.filter(
        owner__username=username).all().order_by('-created_at')
    return repos


def get_repository_by_full_name(full_name):
    try:
        repo = Repository.objects.get(full_name=full_name)
        return repo
    except Repository.DoesNotExist:
        raise Exception('repo not found', status.HTTP_404_NOT_FOUND)


def create_repository(profile, full_name_or_id):
    try:
        g = Github(profile.access_token)
        repo = g.get_repo(full_name_or_id=full_name_or_id)
        hook_id = create_hook(repo)
        new_repository = Repository.objects.create(
            name=repo.name,
            description=repo.description,
            owner=profile,
            hook_id=hook_id
        )

        create_commits_by_repo(repo, new_repository)

        return new_repository

    except db_utils.IntegrityError:
        raise Exception('repo already on the list',
                        status.HTTP_400_BAD_REQUEST)
    except UnknownObjectException:
        raise Exception('repo not found', status.HTTP_404_NOT_FOUND)
    except Exception as e:
        message, status_code = e.args
        raise Exception(message, status_code)


def create_commits(*commits):
    try:
        Commit.objects.bulk_create(*commits)
    except db_utils.IntegrityError as e:
        raise Exception('commit already on the list',
                        status.HTTP_400_BAD_REQUEST)


def create_commits_by_repo(github_repo, repo_object):
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

        create_commits(commit_list)
    except db_utils.IntegrityError:
        raise Exception('commit already on the list',
                        status.HTTP_400_BAD_REQUEST)


def get_commits_by_repo(repo_full_name):
    commits = Commit.objects.filter(
        repository__full_name=repo_full_name
    ).all().order_by('-commited_at')

    return commits


def create_hook(repo):
    base_url = 'https://github-monitor-app.herokuapp.com'
    hook_url = reverse('monitor:push-event')
    config = {
        'url': f'{base_url}{hook_url}',
        'content_type': 'json'
    }
    events = ['push']
    try:
        hook = repo.create_hook('web', config, events, active=True)
        return hook.id
    except GithubException as e:
        return None


class MonitorPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
