from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError

from eforce_api.models import SummmarizedCrisisUpdate, Crisis
from eforce_front.exceptions import UpdateCrisisCMOError
from eforce.settings import CONST_CMO_DOMAIN

import requests


def send_and_create_cmo_sum_update(request):

    sum_update_title = request.POST.get('sum_update_title', '')
    sum_update_desc = request.POST.get('sum_update_desc', '')
    sum_update_force_lat = request.POST.get('sum_update_force_lat', 0)
    sum_update_force_lng = request.POST.get('sum_update_force_lng', 0)
    sum_update_force_size = request.POST.get('sum_update_force_size', 0)
    sum_update_force_casualty = request.POST.get('sum_update_force_casualty', 0)
    sum_update_known_casualty = request.POST.get('sum_update_known_casualty', 0)
    sum_update_known_dead = request.POST.get('sum_update_known_dead', 0)
    sum_update_for_crisis = request.POST.get('sum_update_for_crisis', None)
    sum_update_crisis_resolved = request.POST.get('sum_update_crisis_resolved', False)

    if sum_update_for_crisis.strip() == '':
        raise UpdateCrisisCMOError(error="Crisis not selected when sending CMO update.")
    if not sum_update_title:
        raise UpdateCrisisCMOError(error="Crisis update title must not be empty.")
    if not sum_update_desc:
        raise UpdateCrisisCMOError(error="Crisis update description must not be empty.")

    try:
        for_crisis = Crisis.objects.get(pk=sum_update_for_crisis)
    except ObjectDoesNotExist:
        raise UpdateCrisisCMOError(error="The crisis selected does not exist.")

    sum_update_cmo_crisis_id = for_crisis.cmo_crisis_id

    api_url = "cmowebservice/operationupdate.aspx"
    payload = {'Incident_ID': sum_update_cmo_crisis_id,
               'Force_Size': sum_update_force_size,
               'Force_Casualty': sum_update_force_casualty,
               'Force_lat': sum_update_force_lat,
               'Force_long': sum_update_force_lng,
               'Known_Casualty': sum_update_known_casualty,
               'Known_Dead': sum_update_known_dead
               }

    send_update_success = False
    r = requests.get(CONST_CMO_DOMAIN + api_url, data=payload)
    if r.text.strip() == '1':
        send_update_success = True

    if sum_update_crisis_resolved:
        sum_update_desc = sum_update_desc + '\n' + "The crisis was resolvd."

    api_url = "cmowebservice/responseincidentchat.aspx"
    payload = {'Incident_ID': sum_update_cmo_crisis_id,
               'Sender': request.user.userprofile.get_readable_groupname(),
               'Description': sum_update_desc
               }

    r = requests.get(CONST_CMO_DOMAIN + api_url, data=payload)
    print("'" + r.text + "'")

    try:
        with transaction.atomic():
            if send_update_success and sum_update_crisis_resolved:
                for_crisis.resolve = True
                for_crisis.save()
            SummmarizedCrisisUpdate.objects.create(
                title=sum_update_title,
                description=sum_update_desc,
                force_lat=sum_update_force_lat,
                force_lng=sum_update_force_lng,
                force_size=sum_update_force_size,
                force_casualty=sum_update_force_casualty,
                known_casualty=sum_update_known_casualty,
                known_dead=sum_update_known_dead,
                for_crisis=for_crisis
            )
    except IntegrityError as e:
        raise UpdateCrisisCMOError(error="Something very bad has just happen.")
