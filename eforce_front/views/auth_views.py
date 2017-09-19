from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from eforce_front.exceptions import AuthenticationError
import re


def try_login_user(request, username, password):

    if not (username and password):
        raise AuthenticationError(error='Sign-in credentials not entered.')

    email_regex_pattern = '^([\w\.]+)@((?:[\w]+\.)+)([a-zA-Z]{2,4})$'
    if re.search(email_regex_pattern, username) is not None:
        try:
            username = User.objects.get(email=username).username
        except User.DoesNotExist:
            username = None

    user = authenticate(username=username, password=password)
    if user is None:
        raise AuthenticationError(error='Incorrect sign-in credentials provided.')

    if not user.is_active:
        raise AuthenticationError(error='The account is currently disabled.')

    if user.userprofile.usergroup is None:
        raise AuthenticationError(error='This user is not registered with any EF group yet.')

    login(request, user)
    return True
