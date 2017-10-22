from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from django.contrib.auth.models import User

from eforce.settings import EF_HQ_ROLENAME

# FOR AIRLINEAPP
import json
AIRLINEAPP_TRACKER = {}


@channel_session_user_from_http
def ws_connect_efhq(message):

    if not message.user.userprofile.is_EF_HQ_user():
        return

    message.reply_channel.send({"accept": True})
    Group('efhq').add(message.reply_channel)


@channel_session_user_from_http
def ws_connect_efassets(message):

    if message.user.userprofile.is_EF_HQ_user():
        return

    message.reply_channel.send({"accept": True})
    Group('efassets').add(message.reply_channel)


@channel_session_user_from_http
def ws_disconnect_hq(message):
    Group('efhq').discard(message.reply_channel)


@channel_session_user_from_http
def ws_disconnect_efassets(message):
    Group('efassets').discard(message.reply_channel)


# FOR AIRLINEAPP
@channel_session
def ws_connect_airlinechat(message):
    Group("airlineapp").add(message.reply_channel)
    numPeople = len(Group("airlineapp").channel_layer.group_channels("airlineapp"))
    Group("airlineapp").send({
        "text": json.dumps({
            "type": "usersConnected",
            "usersConnected": numPeople
        })
    })


@channel_session
def ws_receive_airlinechat(message):
    sessKey = message.channel_session.session_key
    chatUser = json.loads(message['text'])
    AIRLINEAPP_TRACKER[sessKey] = chatUser
    Group("airlineapp").send({
        "text": json.dumps({
            "type": "chatUsersDetails",
            "chatUsersDetails": AIRLINEAPP_TRACKER
        })
    })


@channel_session
def ws_disconnect_airlinechat(message):
    sessKey = message.channel_session.session_key
    Group('airlineapp').discard(message.reply_channel)
    del AIRLINEAPP_TRACKER[sessKey]

    numPeople = len(Group("airlineapp").channel_layer.group_channels("airlineapp"))
    Group("airlineapp").send({
        "text": json.dumps({
            "type": "usersConnected",
            "usersConnected": numPeople
        })
    })
