from django.shortcuts import redirect
from django_hosts import reverse

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
