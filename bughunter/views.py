import logging

from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('khromoff.bugs')


@csrf_exempt
def report(request):
    # saves bugreport to database and sends message to admin
    # (e.g. creates a log entry)

    if request.method == 'POST':
        if request.POST.get('location') is None:
            return HttpResponse('What? How did you just do that? Are you an ad? If you are not, please report this.')

        logger.warning('New bugreport:\n'
                       'page: %s\n'
                       'user_ip: %s\n'
                       'user: %s\n'
                       'error_type: %s\n'
                       'description: %s'
                       % (request.POST.get('location'), request.META['REMOTE_ADDR'],
                          request.user, request.POST.get('error_type'), request.POST.get('description')))
        
        # TODO: save in DB, create page about it. more info there
        return HttpResponse('thx doode')
    else:
        raise Http404
