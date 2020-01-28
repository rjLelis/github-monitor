import requests
from decouple import config
from django.shortcuts import redirect, render
from django.contrib import messages
from monitor import helpers as monitor_helpers
from . import helpers as auth_helpers
from github import Github


@auth_helpers.logout_required
def index(request):
    return render(request, 'auth_access/index.html')


@auth_helpers.login_required
def logout(request):
    return auth_helpers.execute_logout(request)


@auth_helpers.logout_required
def get_token(request):
    # Todo: Create validations in case code and access_token return empty
    payload = {
        'code': request.GET.get('code'),
        'client_id': config('CLIENT_ID'),
        'client_secret': config('CLIENT_SECRET')
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    access = requests.post(
        'https://github.com/login/oauth/access_token',
        json=payload,
        headers=headers
    ).json()
    access_token = access.get('access_token')

    g = Github(access_token)
    user = g.get_user()

    profile, _ = monitor_helpers.create_profile(
        username=user.login,
        name=user.name,
        email=user.email,
        access_token=access_token
    )

    auth_helpers.execute_login(request, profile.username)

    return redirect('frontend:index')


@auth_helpers.logout_required
def redirect_access(request):
    username = request.POST.get('username')

    if not username:
        messages.error(request, 'Enter your Github username', extra_tags='danger')
        return redirect('auth:index')

    client_id = config('CLIENT_ID')

    client_id = f'client_id={client_id}'
    login = f'login={username}'
    scopes = 'scope=write:repo_hook,repo'
    params = [
        client_id,
        login,
        scopes
    ]

    auth_url = f'https://github.com/login/oauth/authorize?'
    for param in params:
        auth_url += f'&{param}'

    return redirect(auth_url)
