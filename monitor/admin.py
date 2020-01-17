from django.contrib import admin
from .models import Profile, Repository, Commit


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('access_token', )


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    readonly_fields = ('full_name', )


admin.site.register(Commit)
