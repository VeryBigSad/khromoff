# file with static shit we need in processing


def static_context(request):
    context = {'static': {
        # TODO: rename to https
        'HOSTNAME': 'http://' + request.META['HTTP_HOST']
    }}
    return context


