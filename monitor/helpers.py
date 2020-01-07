from .models import Profile


def create_profile(**kwargs):
    profile, created = Profile.objects.get_or_create(**kwargs)
    return (created, profile)


def get_profile(**login_or_token):
    try:
        profile = Profile.objects.get(**login_or_token)
        return (True, profile)
    except Profile.DoesNotExist:
        return (False, None)
    except Exception as e:
        raise e
