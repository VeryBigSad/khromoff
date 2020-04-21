from khromoff.settings import DEBUG


def static_context(request):
    # some basic stuff

    context = {'static': {
        'HOSTNAME': request.META['HTTP_HOST']
    }}
    return context


def debug(request):
    return {'debug': DEBUG}
