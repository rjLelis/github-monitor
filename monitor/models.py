from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    access_token = models.CharField(max_length=40, null=True)

    def __str__(self):
        return f'{self.name} <{self.username}>'


class Repository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='repositories'
    )

    def __str__(self):
        return f'{self.owner.username}/{self.name}'


class Commit(models.Model):
    sha = models.CharField(max_length=40, unique=True)
    commiter = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL,
        related_name='commits'
    )
    commited_at = models.DateTimeField()
    message = models.TextField()
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name='commits'
    )

    def __str__(self):
        return f'{self.message} {self.sha[:7]}'
