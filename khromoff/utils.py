from django.shortcuts import redirect
from django_hosts import reverse
from django_log_to_telegram.log import AdminTelegramHandler, TelegramFormatter

from khromoff.settings import DOMAIN_NAME


def next_redirect_or_main(request):
    """
    if possible (and safe) redirects to GET.NEXT parameter
    
    :param request: django request object
    :return: redirect to the ?NEXT param in GET
    """
    if request.GET.get('next'):
        if DOMAIN_NAME in request.GET.get('next') or '.' not in request.GET.get('next'):
            return redirect(request.GET['next'])
    return redirect(reverse('index', host='index'))


class TelgramLogFormatter(TelegramFormatter):
    def format(self, record):
        try:
            a = 'ERROR: http500 page:\n' + super().format(record) + '\n'
            request = record.request
            a += 'view_name: %s\n' % request.resolver_match.view_name
            a += 'POST data: %s\n' % dict(request.POST)
            a += 'GET data: %s' % dict(request.GET)
        except AttributeError:
            a = record.message

        return str(a)


class TelegramLogHandler(AdminTelegramHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFormatter(TelgramLogFormatter())
