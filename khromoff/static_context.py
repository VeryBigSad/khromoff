# file with static shit we need in processing


def static_context(request):
    context = {'static': {
        'HOSTNAME': 'http://127.0.0.1'
    }}
    return context


