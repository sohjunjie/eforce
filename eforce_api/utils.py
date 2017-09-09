from django.core.exceptions import ObjectDoesNotExist
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
