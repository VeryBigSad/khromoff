import os

import requests
from django.shortcuts import redirect
from django_hosts import reverse

from khromoff.settings import DOMAIN_NAME


def check_captcha(hcaptcha_response):
    errors = []

    data = {'secret': os.getenv("HCAPTCHA_SECRET_KEY"), 'response': hcaptcha_response}
    resp = requests.post('https://hcaptcha.com/siteverify', data=data).json()
    if not resp['success']:
        captcha_errors = []
        try:
            captcha_errors = resp['error-codes']
        except KeyError:
            errors.append(
                {'type': 'captcha', 'description':
                    'Произошла ошибка с капчей, попробуйте снова.'}
            )
        for i in captcha_errors:
            if i == 'missing-input-response':
                errors.append(
                    {'type': 'captcha',
                     'description': 'Пожалуйста, введите капчу.'}
                )
            elif i == 'invalid-input-response':
                errors.append(
                    {'type': 'captcha',
                     'description': 'Произошла ошибка с капчей, попробуйте снова.'}
                )
            else:
                raise Exception('Произошла ошибка при проверки капчи.')
    return errors


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
