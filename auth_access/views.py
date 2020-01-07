import requests
from decouple import config
from django.shortcuts import redirect
from monitor.helpers import create_profile, get_profile
from github import Github


def get_token(request):
    # Todo: Create validations in case code and access_token return empty
    payload = {
        'code': request.GET.get('code'),
        'client_id': config('CLIENT_ID'),
        'client_secret': config('CLIENT_SECRET')
    }

    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }

    access = requests.post(
        'https://github.com/login/oauth/access_token',
        data=payload,
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

    request.session['access_token'] = access_token
    request.session['username'] = profile.username

    return redirect('frontend:index', request)


def redirect(request):
    username = request.GET.get('username')
    found_profile, profile = get_profile(username)

    if found_profile:
        request.session['access_token'] = profile.access_token
        request.session['username'] = profile.username
        return redirect('frontend:index', request)

    client_id = config('CLIENT_ID')
    auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&login={username}'

    return redirect(auth_url, request)
