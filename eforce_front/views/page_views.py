from .auth_views import try_login_user
from .get_context_views import get_user_group_crisis_instructions, get_this_efasset_usergroup_sent_updates_by_page
from .cmo_comm_api_views import send_and_create_cmo_sum_update, \
    send_and_create_efhq_ground_update, send_and_create_dispatch_efassets_instruction

from eforce_api.models import Crisis
from eforce_api.utils import PermissionManager
from eforce_front.exceptions import AuthenticationError, UpdateCrisisCMOError, \
    UpdateCrisisEFHQError, DispatchEFAssetsError

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
@PermissionManager.EF_HQ_required
def go_to_dispatch_ef_page(request):

    if not request.POST:
        return render(request, 'home/ef_hq/dispatch_ef.html')

    try:
        send_and_create_dispatch_efassets_instruction(request)
        messages.success(request, "Your dispatch instructions was successfully sent.")
    except DispatchEFAssetsError as e:
        messages.error(request, e.error)

    return render(request, 'home/ef_hq/dispatch_ef.html')


@login_required
@PermissionManager.EF_HQ_required
def go_to_manage_crisis_page(request):
    return render(request, 'home/ef_hq/manage_crisis.html')


@login_required
@PermissionManager.EF_HQ_required
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

@login_required
@PermissionManager.EF_Assets_required
def go_to_update_hq_page(request):

    if not request.POST:
        return render(request, 'home/ef_assets/update_hq.html')

    try:
        send_and_create_efhq_ground_update(request)
        messages.success(request, "Summary update has been successfully send to HQ.")
    except UpdateCrisisEFHQError as e:
        messages.error(request, e.error)

    return render(request, 'home/ef_assets/update_hq.html')


@login_required
@PermissionManager.EF_Assets_required
def go_to_efassets_view_sent_update_page(request):
    paged_sent_updates = get_this_efasset_usergroup_sent_updates_by_page(request)
    return render(request, 'home/ef_assets/view_sent_groundupdate.html', {'sent_updates': paged_sent_updates})


@login_required
@PermissionManager.usergroup_required
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
