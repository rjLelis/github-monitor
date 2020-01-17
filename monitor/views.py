from rest_framework import generics

from .models import Repository
from .serializers import RepositorySerializer
from auth_access import helpers as auth_helpers


class RepositoryListCreatView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    authentication_classes = (auth_helpers.GithubAuthentication, )
