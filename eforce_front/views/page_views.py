from .auth_views import try_login_user
from eforce_front.exceptions import AuthenticationError

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect

import re


# TODO: REFACTOR POST LOGIN INTO AUTH_VIEWS.PY
def index(request, redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, reverse('ef-home')))

    if request.user.is_authenticated():
        return redirect(redirect_to)

    if not request.POST:
        return render(request, 'index/sign-in.html', {'redirect_to': redirect_to})

    username = request.POST.get('username', '').lower()
    password = request.POST.get('password', '')

    try:
        if try_login_user(username, password):
            return redirect(redirect_to)
    except AuthenticationError as e:
        messages.error(request, e.error)
        return redirect(reverse('ef-index'))


@login_required
def homepage(request):
    return render(request, 'index/sign-in.html', {'redirect_to': redirect_to})
