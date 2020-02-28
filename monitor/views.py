from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth_access import helpers as auth_helpers

from . import helpers as monitor_helpers
from . import tasks as monitor_task
from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer


class RepositoryListCreateView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    authentication_classes = (auth_helpers.GithubAuthentication, )

    def get_queryset(self):
        queryset = self.queryset
        if self.request.method == 'GET':
            username = self.request.session.get('username')
            queryset = monitor_helpers.get_repositories_by_user(username)

        return queryset

    def post(self, request, *args, **kwargs):
        username = request.session.get('username')
        serializer = RepositorySerializer(
            data=request.data,
            context={'username': username}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


@api_view(['GET'])
@auth_helpers.login_required
def commits_by_repository(request, repo_name):
    username = request.session.get('username')
    repo_full_name = f'{username}/{repo_name}'
    commits = monitor_helpers.get_commits_by_repo(repo_full_name)

    paginator = monitor_helpers.MonitorPagination()
    return paginator.paginate_function_based_view(
                commits, request, CommitSerializer)


@api_view(['POST'])
def push_event(request):
    repository_info = request.data.pop('repository')
    commits_pushed = request.data.pop('commits')
    sender = request.data.pop('sender')

    monitor_task.insert_pushed_commits(
        repository_info, commits_pushed, sender
    )
