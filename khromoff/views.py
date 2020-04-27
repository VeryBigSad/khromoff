import datetime
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from datetime import datetime

from urlshortner.models import ShortUrl, Visit
from api.models import UserAPIKey

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
        if i not in string.ascii_lowercase + '0123456789-_':
            errors.append({'type': 'invalid_password',
                           'description': 'Пароль должен содержать'
                                          ' только латиницу, цифры, тире и нижнее подчеркивание.'})
            break
    try:
        validate_password(password)
    except ValidationError as e:
        for i in e:
            errors.append({'type': 'weak_password',
                           'description': i})
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
        if i not in string.ascii_lowercase + '0123456789-_':
            errors.append({'type': 'invalid_username',
                           'description': 'Имя пользователя должно содержать'
                                          ' только латиницу, цифры, тире и нижнее подчеркивание.'})
            break

    return errors


def error404(request, exception):
    return render(request, '404error.html', context={'description': str(exception)}, status=404)


def error500(request):
    return render(request, '500error.html', status=500)


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('personal'))

    if request.method == 'POST':
        if request.POST['type'] == 'login':
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            # If invalid session, then delete db and recreate.
            # This user should always exist. Otherwise, idk create it manually, this is TEMP so not coding it :shrug:
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect('/')
            else:
                return render(request, 'login_register.html', context={'errors': [{'type': 'wrong_credentials',
                                                                                   'description': 'Неверный логин или'
                                                                                                  ' пароль.'}],
                                                                       'menu': request.POST['type']})
        elif request.POST['type'] == 'register':
            errors = []
            # TODO: send in post data request.POST so we dont have to refill the fields
            errors += username_valid_checks(request.POST['username'])
            errors += password_valid_checks(request.POST['password'], request.POST['password_repeat'])

            if errors:
                return render(request, 'login_register.html', context={'errors': errors, 'menu': request.POST['type']})

            new_user = User.objects.create_user(request.POST['username'], '', request.POST['password'])
            login(request, new_user)

            if request.GET.get('next') and request.GET.get('next') != '/':
                return redirect(request.GET['next'])
            else:
                return redirect(reverse('personal') + '?new')

        else:
            return HttpResponseServerError()

    elif request.method == 'GET':
        return render(request, 'login_register.html')


@login_required()
def personal(request):
    errors = []
    context = {}

    # TODO: do something with that it only contains 10 last items
    created_shorturls = ShortUrl.objects.filter(author=request.user).order_by('-time_created')[:10]
    created_shorturls = [{'times_visited': len(Visit.objects.filter(shorturl=i)), 'obj': i} for i in
                         created_shorturls]

    keys = UserAPIKey.objects.filter(user=request.user)[:10]
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
    return render(request, 'about.html')


def me(request):
    return render(request, 'me.html', context={'age': datetime.today().year - 2005})


def logout_page(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        return HttpResponseRedirect('/')


def index(request):
    return render(request, 'index.html', context={})
