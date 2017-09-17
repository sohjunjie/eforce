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
