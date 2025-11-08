from django.http import HttpResponse
from ratelimit.decorators import ratelimit


def get_rate_limit_key(group, request):
    """
    Determines the rate limit key.
    Uses the user's primary key if authenticated, otherwise uses their IP address.
    """
    if request.user.is_authenticated:
        return request.user.pk
    return request.META.get('REMOTE_ADDR')


@ratelimit(key=get_rate_limit_key, rate='5/m', block=True, method='GET')
@ratelimit(key=get_rate_limit_key, rate='10/m', block=True, method='GET', group='authenticated_user')
def sensitive_view(request):
    """
    A view that is rate-limited.
    """
    return HttpResponse("This is a sensitive view. Please don't abuse it.")