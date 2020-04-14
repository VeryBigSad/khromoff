# file with static shit we need in processing


def static_context(request):
    context = {'static': {
        'HOSTNAME': request.META['HTTP_HOST']
    }}
    return context


