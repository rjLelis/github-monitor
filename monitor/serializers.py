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
            profile, _ = monitor_helpers.get_profile(username=username)
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

