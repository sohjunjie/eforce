from .auth_views import try_login_user
from eforce_front.exceptions import AuthenticationError

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect

import re


def go_to_signin(request, redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, reverse('home')))

    if request.user.is_authenticated():
        return redirect(redirect_to)

    if not request.POST:
        return render(request, 'index/sign-in.html', {'redirect_to': redirect_to})

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    try:
        if try_login_user(request, username, password):
            return redirect(redirect_to)
    except AuthenticationError as e:
        messages.error(request, e.error)
        return redirect(go_to_signin)


@login_required
def go_to_dispatch_ef_page(request):
    return render(request, 'home/ef_hq/dispatch_ef.html')


def go_to_manage_crisis_page(request):
    return render(request, 'home/ef_hq/manage_crisis.html')


def go_to_update_hq_page(request):
    return render(request, 'home/ef_assets/update_hq.html')


@login_required
def go_to_homepage(request):

    if request.user.userprofile.is_EF_HQ_user():
        render_page = 'home/ef_hq/main.html'
    else:
        render_page = 'home/ef_assets/main.html'

    return render(request, render_page)


def logout_user(request):
    logout(request)
    return redirect(go_to_signin)
