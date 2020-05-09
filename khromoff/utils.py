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
        a = super().format(record)
        r = record.request
        a += '\n'
        a += 'view_name: %s\n' % r.resolver_match.view_name
        a += 'POST data: %s\n' % dict(r.POST)
        a += 'GET data: %s\n' % dict(r.GET)

        return str(a)


class TelegramLogHandler(AdminTelegramHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFormatter(TelgramLogFormatter())
