from celery import task

from . import helpers as monitor_helpers
from .models import Commit


@task()
def insert_pushed_commits(repository, commits, sender):
    try:
        repo_full_name = repository.get('full_name')
        repository = monitor_helpers.get_repository_by_full_name(
            repo_full_name)

        sender_username = sender.get('login')
        profile = monitor_helpers.create_profile(username=sender_username)

        commits = []
        for commit in commits:
            new_commit = Commit(
                sha=commit.get('id'),
                commiter=profile,
                commited_at=commit.get('timestamp'),
                message=commit.get('message'),
                repository=repository
            )
            commits.append(new_commit)

        monitor_helpers.create_commits(commits)
        print('Created')
    except Exception as e:
        print('Error ', e)
        return None
