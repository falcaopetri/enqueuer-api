from userena.utils import get_user_profile

def get_users_profiles(users):
    """
        Gets the User profile associated to each of
        the django-userena's users on $users
    """
    users_profiles = [get_user_profile(user) for user in users]
    return users_profiles
