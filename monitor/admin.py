from django.contrib import admin
from .models import Profile, Repository, Commit

admin.site.register(Profile)
admin.site.register(Repository)
admin.site.register(Commit)
