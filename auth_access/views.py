import requests
from decouple import config
from django.shortcuts import redirect, render
from monitor.helpers import create_profile, get_profile
from .helpers import login
from github import Github


def index(request):
    if 'access_token' in request.session:
        return redirect('frontend:index')
    return render(request, 'auth_access/index.html')


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

    created, profile = create_profile(
      username=user.login,
      name=user.name,
      email=user.email,
      access_token=access_token
    )

    execute_login(request, access_token, profile.username)

    return redirect('frontend:index')


def redirect_access(request):
    username = request.POST.get('username')
    found_profile, profile = get_profile(username=username)

    if found_profile:
        execute_login(request, profile.access_token, profile.username)
        return redirect('frontend:index')

    client_id = config('CLIENT_ID')
    auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&login={username}'

    return redirect(auth_url)
