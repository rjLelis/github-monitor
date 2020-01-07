from django.shortcuts import redirect
from django.contrib.auth import mixins
from rest_framework.authentication import BaseAuthentication
from monitor.models import Profile


def execute_login(request, access_token, username):
    request.session['access_token'] = access_token
    request.session['username'] = username


def login_required(function):
    def wrapper(request, **kwargs):
        if 'access_token' not in request.session:
            return redirect('auth:index')
        return function(request, **kwargs)
    return wrapper


class GithubAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if 'access_token' not in request.session:
            return None

        acces_token = request.session.get('access_token')
        try:
            profile = Profile.objects.get(acces_token=acces_token)
            return (profile, None)
        except Profile.DoesNotExist:
            return None
