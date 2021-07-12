import datetime
import string
from datetime import datetime

import requests
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.utils.translation import gettext
from django_hosts import reverse

from api.models import UserAPIKey
from khromoff.utils import next_redirect_or_main, check_captcha
from urlshortner.models import ShortUrl, Visit

User = get_user_model()


# functions for username and password validation on symbols
def password_valid_checks(password, password_repeat):
    errors = []

    if password != password_repeat:
        errors.append({'type': 'password_not_match',
                       'description': 'Введнные пароли не совпадают.'})
    if len(password) >= 100:
        errors.append({'type': 'password_too_long',
                       'description': 'Пароль не может быть длиннее 100 символов.'})
    for i in password.lower():
        if i not in string.ascii_lowercase + '0123456789_':
            errors.append({'type': 'invalid_password',
                           'description': 'Пароль должен содержать'
                                          ' только латиницу, цифры и нижнее подчеркивание.'})
            break
    try:
        validate_password(password)
    except ValidationError as e:
        for i in e:
            errors.append({'type': 'weak_password',
                           'description': gettext(i)})
    return errors


def username_valid_checks(username):
    errors = []

    if User.objects.filter(username=username).exists():
        errors.append({'type': 'user_exists',
                       'description': 'Пользователь с данным логином уже существует,'
                                      ' попробуйте выбрать другой.'})
    if 31 < len(username) <= 5:
        errors.append({'type': 'invalid_username',
                       'description': 'Имя пользователя должно'
                                      ' быть длинной от 5 до 30 символов.'})
    for i in username.lower():
        if i not in string.ascii_lowercase + '0123456789_':
            errors.append({'type': 'invalid_username',
                           'description': 'Имя пользователя должно содержать'
                                          ' только латиницу, цифры и нижнее подчеркивание.'})
            break
    return errors


def error404(request, exception):
    return render(request, '404error.html', context={'description': str(exception)}, status=404)


def error403(request, exception=None):
    return render(request, '403error.html', status=403)


def error500(request):
    return render(request, '500error.html', status=500)


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('personal', host='index'))

    if request.method == 'POST':
        if request.POST['type'] == 'login':
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                return next_redirect_or_main(request)
            else:
                return render(request, 'login_register.html',
                              context={'errors': [{'type': 'wrong_credentials',
                                                   'description': 'Неверный логин или пароль.'}],
                                       'menu': request.POST['type']})
        elif request.POST['type'] == 'register':
            errors = []
            errors += username_valid_checks(request.POST['username'])
            errors += password_valid_checks(request.POST['password'], request.POST['password_repeat'])

            errors += check_captcha(request.POST['h-captcha-response'])

            if errors:
                return render(request, 'login_register.html', context={'errors': errors, 'menu': request.POST['type']})

            new_user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return next_redirect_or_main(request)

        else:
            return HttpResponseServerError()

    else:
        return render(request, 'login_register.html')


@login_required()
def personal(request):
    errors = []
    context = {}

    # TODO: do something with that it only contains 10 last items
    # TODO: use serializers, not db requests
    created_shorturls = ShortUrl.objects.get_valid_urls().filter(author=request.user).order_by('-time_created')[:10]
    created_shorturls = [{'times_visited': len(Visit.objects.filter(shorturl=i)), 'obj': i} for i in
                         created_shorturls]

    keys = UserAPIKey.objects.get_usable_keys().filter(user=request.user)[:10]
    context['keys'] = keys
    context['created_shorturls'] = created_shorturls

    if request.method == 'POST':
        if request.POST['type'] == 'change_username':
            errors += username_valid_checks(request.POST['new_name'])
            if not errors:
                request.user.username = request.POST['new_name']
                request.user.save()
                context['success'] = 'Имя пользователя успешно изменено!'

        elif request.POST['type'] == 'change_password':
            errors += password_valid_checks(request.POST['new_password'], request.POST['new_password_repeat'])

            if not errors:
                request.user.set_password(request.POST['new_password'])
                request.user.save()

                context['success'] = 'Пароль успешно изменен!'
        context['errors'] = errors

        return render(request, 'personal.html', context=context)

    else:
        return render(request, 'personal.html', context=context)


def about(request):
    last_update_date = cache.get_or_set('last_site_update', (lambda: datetime.strptime(
        requests.get('https://api.github.com/repos/verybigsad/khromoff').json()['updated_at'],
        '%Y-%m-%dT%H:%M:%Sz').strftime('%d.%m.%Y')))
    return render(request, 'about.html', context={'last_update_date': gettext(last_update_date)})


def me(request):
    return render(request, 'me.html', context={'age': datetime.today().year - 2005})


def logout_page(request):
    logout(request)
    return next_redirect_or_main(request)


def index(request):
    return render(request, 'index.html', context={})
