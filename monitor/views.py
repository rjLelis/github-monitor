from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from auth_access import helpers as auth_helpers

from . import helpers as monitor_helpers
from .models import Repository
from .serializers import RepositorySerializer, CommitSerializer


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

    def create(self, request, *args, **kwargs):
        username = request.session.get('username')
        serializer = RepositorySerializer(
            data=request.data,
            context={'username': username}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


@api_view(['GET'])
@auth_helpers.login_required
def commits_by_repository(request, repo_name):
    username = request.session.get('username')
    repo_full_name = f'{username}/{repo_name}'
    commits = monitor_helpers.get_commits_by_repo(repo_full_name)
    serializer = CommitSerializer(commits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
