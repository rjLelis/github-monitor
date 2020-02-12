from rest_framework import serializers

from . import helpers as monitor_helpers
from .models import Commit, Profile, Repository


class RepositorySerializer(serializers.ModelSerializer):
    repository = serializers.CharField(write_only=True)

    class Meta:
        model = Repository
        fields = (
            'id',
            'name',
            'description',
            'repository',
            'full_name'
        )
        extra_kwargs = {
            'description': {'read_only': True},
            'name': {'read_only': True},
            'full_name': {'read_only': True}
        }

    def create(self, validated_data):
        username = self.context.get('username')
        repository_name = validated_data.pop('repository')
        try:
            profile = monitor_helpers.get_profile(username=username)
            new_repository = monitor_helpers.create_repository(
                profile,
                f'{username}/{repository_name}'
            )

        except Exception as e:
            message, status_code = e.args
            validation_error = serializers.ValidationError(detail=message)
            validation_error.status_code = status_code
            raise validation_error

        return new_repository


class CommitSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='commiter.username',
        read_only=True
    )

    author_email = serializers.CharField(
        source='commiter.email',
        read_only=True,
    )

    date = serializers.DateTimeField(
        source='commited_at',
        read_only=True
    )

    class Meta:
        model = Commit
        fields = (
            'sha',
            'author_username',
            'author_email',
            'date',
            'message'
        )
        extra_kwargs = {
            'sha': {'read_only': True},
            'message': {'read_only': True}
        }
