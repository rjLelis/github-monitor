from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from auth_access import helpers as auth_helpers

from . import helpers as monitor_helpers
from .models import Repository
from .serializers import RepositorySerializer


class RepositoryListCreateView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    authentication_classes = (auth_helpers.GithubAuthentication, )

    def get_queryset(self):
        queryset = self.queryset
        if self.request.method == 'GET':
            username = self.request.session.get('username')
            queryset = monitor_helpers.get_repositories_by_username(username)

        return queryset

    def create(self, request, *args, **kwargs):
        username = request.session.get('username')
        serializer = RepositorySerializer(
            data=request.data,
            context={'username': username}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

