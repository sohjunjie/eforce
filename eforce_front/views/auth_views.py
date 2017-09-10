from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from eforce_front.exceptions import AuthenticationError
import re


def try_login_user(username, password):

    if not (username and password):
        raise AuthenticationError(error='Sign-in credentials not entered.')

    email_regex_pattern = '^([\w\.]+)@((?:[\w]+\.)+)([a-zA-Z]{2,4})$'
    if re.search(email_regex_pattern, username) is not None:
        try:
            username = User.objects.get(email=username).username
        except User.DoesNotExist:
            username = None

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        else:
            raise AuthenticationError(error='The account is currently disabled.')
    else:
        raise AuthenticationError(error='Incorrect sign-in credentials provided.')

    raise AuthenticationError(error='Unable to sign-in.')
