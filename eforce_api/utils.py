from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from rest_framework import status

import json


def get_request_body_param(request, param, return_on_error):

    body_unicode = request.body.decode('utf-8')

    try:
        j = json.loads(body_unicode)
    except json.decoder.JSONDecodeError:
        return return_on_error

    try:
        return j[param]
    except KeyError:
        return return_on_error


class PermissionManager:
    def usergroup_required(function):

        def wrap(request, *args, **kwargs):

            if request.user.is_authenticated():                 # via basic authentication
                u = request.user
                if u.userprofile.usergroup is not None:
                    return function(request, *args, **kwargs)
                return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

            return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap

    def EF_HQ_required(function):

        def wrap(request, *args, **kwargs):

            if request.user.is_authenticated():                 # via basic authentication
                u = request.user
                if (u.userprofile.usergroup is not None) and (u.userprofile.is_EF_HQ_user()):
                    return function(request, *args, **kwargs)
                return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

            return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap

    def EF_Assets_required(function):

        def wrap(request, *args, **kwargs):

            if request.user.is_authenticated():                 # via basic authentication
                u = request.user
                if (u.userprofile.usergroup is not None) and (not u.userprofile.is_EF_HQ_user()):
                    return function(request, *args, **kwargs)
                return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

            return JsonResponse({"Success": False}, status=status.HTTP_403_FORBIDDEN)

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
