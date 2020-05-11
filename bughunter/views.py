import logging

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('khromoff.bugs')


@csrf_exempt
def report(request):
    # saves bugreport to database and sends message to admin
    # (e.g. creates a log entry)
    # cache.set('my_key', 'hello, world!', 60 * 60)  # one hour
    # cache.set(request.META['REMOTE_ADDR'], 'reported', 6 * 3600)

    if request.method == 'POST':
        logger.info('New bugreport:\n'
                    'page: %s\n'
                    'user_ip: %s\n'
                    'user: %s\n'
                    'error_type: %s'
                    % (request.build_absolute_uri(), request.META['REMOTE_ADDR'],
                       request.user, request.POST.get('error_type')))
        # TODO: save in DB, create page about it. more info there
        return HttpResponse('thx doode')
    else:
        raise Http404
