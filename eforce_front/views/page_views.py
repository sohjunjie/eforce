from .auth_views import try_login_user
from .get_context_views import get_user_group_crisis_instructions
from .cmo_comm_api_views import send_and_create_cmo_sum_update, send_and_create_efhq_ground_update

from eforce_api.models import Crisis
from eforce_front.exceptions import AuthenticationError, UpdateCrisisCMOError, UpdateCrisisEFHQError

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


@login_required
def go_to_manage_crisis_page(request):
    return render(request, 'home/ef_hq/manage_crisis.html')


@login_required
def go_to_update_cmo_page(request):

    if not request.POST:
        return render(request, 'home/ef_hq/update_cmo.html')

    try:
        send_and_create_cmo_sum_update(request)
        messages.success(request, "Summary update has been successfully send to CMO.")
    except UpdateCrisisCMOError as e:
        messages.error(request, e.error)

    return render(request, 'home/ef_hq/update_cmo.html')


# https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=14&size=400x400&key={api_key}
# https://www.google.com.sg/maps/dir//1.3526699,103.8206117/@1.3486369,103.8144319,13z

@login_required
def go_to_update_hq_page(request):

    if not request.POST:
        return render(request, 'home/ef_assets/update_hq.html')

    try:
        send_and_create_efhq_ground_update(request)
        messages.success(request, "Summary update has been successfully send to CMO.")
    except UpdateCrisisEFHQError as e:
        messages.error(request, e.error)

    return render(request, 'home/ef_assets/update_hq.html')


@login_required
def go_to_efassets_sent_groundupdate_page(request):
    return render(request, 'home/ef_assets/view_sent_groundupdate.html')


@login_required
def go_to_homepage(request):

    if request.user.userprofile.is_EF_HQ_user():
        render_page = 'home/ef_hq/main.html'
        context = {'crisises': Crisis.objects.all()}
    else:
        render_page = 'home/ef_assets/main.html'
        crisis_instructions = get_user_group_crisis_instructions(request.user)
        context = {'crisis_instructions': crisis_instructions}

    return render(request, render_page, context)


def logout_user(request):
    logout(request)
    return redirect(go_to_signin)
