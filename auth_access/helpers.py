from django.shortcuts import redirect
from django.contrib.auth import mixins
from django.contrib import messages
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from monitor import helpers as monitor_helpers


def execute_login(request, username):
    request.session['username'] = username


def execute_logout(request):
    try:
        del request.session['username']
        messages.success(request, 'You have been logged out')
        return redirect('auth:index')
    except KeyError:
        pass


def logout_required(function):
    def wrapper(request, **kwargs):
        if 'username' in request.session:
            return redirect('frontend:index')
        return function(request, **kwargs)
    return wrapper


def login_required(function):
    def wrapper(request, **kwargs):
        if 'username' not in request.session:
            return redirect('auth:index')
        return function(request, **kwargs)
    return wrapper


class GithubAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if 'username' not in request.session:
            raise AuthenticationFailed('user not logged in')

        username = request.session.get('username')
        try:
            profile, _ = monitor_helpers.get_profile(username=username)
            return profile, None
        except Exception:
            raise AuthenticationFailed('user not logged in')

