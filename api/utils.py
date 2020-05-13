# from rest_framework.views import exception_handler
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, throttling
from rest_framework import exceptions
from rest_framework.response import Response as _Response

from api.models import UserAPIKey


class APITokenAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'POST':
            token = request.POST.get('token')
        else:
            token = request.GET.get('token')

        if not token:
            # if wasn't specified or not GET or POST
            return None

        try:
            api_key = UserAPIKey.objects.get_from_key(token)
        except UserAPIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return AnonymousUser, {'key': api_key}


class UserAPIKeyThrottle(throttling.SimpleRateThrottle):
    """
        Throttle for API keys
    """

    def get_rate(self):
        return None

    def __init__(self):
        self.rate = None
        self.num_requests = None
        self.duration = 60  # always per-minute

    def get_cache_key(self, request, view):
        try:
            if request.auth:
                # key
                ident = request.auth
            else:
                # not a API KEY request, so ignore it
                return None
        except AttributeError:
            # not a API KEY request, so ignore it
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request, view):
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        try:
            if request.auth:
                # key
                key = request.auth['key']
            else:
                # not a API KEY request, so ignore it
                return True
        except AttributeError:
            # not a API KEY request, so ignore it
            return True

        self.num_requests = key.requests_per_minute

        # Drop any requests from the history which have now passed the
        # throttle duration

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return False
        return self.throttle_success()

    def wait(self):
        return None


class ParamRequired(exceptions.APIException):
    detail = 'Required parameter not specified'
    code = 'params_required'

    def get_codes(self):
        return self.code


def Response(thing, status=200, **kwargs):
    if status == 200:
        return _Response({'response': thing}, **kwargs)
    else:
        return _Response({'error': thing}, status=status, **kwargs)

