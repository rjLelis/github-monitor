from .models import Profile


def create_profile(**profile):
    profile, created = Profile.objects.get_or_create(**profile)
    if not created:
        profile.name = profile.get('username', profile.name)
        profile.email = profile.get('email', profile.email)
        profile.access_token = profile.get('access_token', profile.access_token)
        profile.save()

    return (profile, created)


def get_profile(**login_or_token):
    try:
        profile = Profile.objects.get(**login_or_token)
        found = True
        return (profile, found)
    except Profile.DoesNotExist:
        found = False
        return (None, found)
    except Exception as e:
        raise e
