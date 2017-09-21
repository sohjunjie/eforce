from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.simple_tag
def google_api_key():
    from eforce.settings import GOOGLE_SERVICE_API_KEY
    return GOOGLE_SERVICE_API_KEY


@register.simple_tag
def ef_assets_user_instructions(user):
    from eforce_front.views.get_context_views import get_user_group_unread_instructions
    return get_user_group_unread_instructions(user)


@register.simple_tag
def get_humanize_datetime(datetime):
    import humanize
    from django.utils import timezone
    return humanize.naturaltime(timezone.now() - datetime)
