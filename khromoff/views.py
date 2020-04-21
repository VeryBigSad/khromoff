import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from khromoff.settings import DEBUG

from datetime import datetime


def error404(request, exception):
    return render(request, '404error.html', status=404)


def error500(request):
    return render(request, '500error.html', status=500)


def login_page(request):
    if request.GET.get('guest') == '' and DEBUG:
        user = authenticate(username='guest', password='dickerydick')
        # If invalid session, then delete db and recreate.
        # This user should always exist. Otherwise, idk create it manually, this is TEMP so not coding it :shrug:
        login(request, user)
    else:
        return render(request, 'login_register.html')

    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        return HttpResponseRedirect('/')


@login_required()
def personal(request):
    return render(request, 'personal.html')


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

