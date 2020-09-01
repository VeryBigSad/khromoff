from khromoff.settings import DEBUG, PARENT_HOST


def static_context(request):
    # some basic stuff

    context = {'static': {
        'HOSTNAME': request.META['HTTP_HOST'].replace('http://', 'https://'),
        'HOST': PARENT_HOST
    }}
    return context


def debug(request):
    return {'debug': DEBUG}


def is_subdomain(request):
    if request.get_host().split(':')[0] != PARENT_HOST:
        return {'is_subdomain': True}
    return {'is_subdomain': False}
