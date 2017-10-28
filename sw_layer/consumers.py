from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

from django.contrib.auth.models import User

from eforce.settings import EF_HQ_ROLENAME


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
