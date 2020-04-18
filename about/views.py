from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


@login_required()
def cabinet(request):
    return render(request, 'cabinet.html')


def index(request):
    return render(request, 'index.html', context={})


def about(request):
    return render(request, 'about.html', context={})


def login_page(request):
    if request.GET.get('guest') == '':
        user = authenticate(username='guest', password='dickerydick')

        # If invalid session, then delete db and recreate.

        # This user should always exist. Otherwise, idk create it manually, this is TEMP so not coding it :shrug:
        login(request, user)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        return HttpResponseRedirect('/')


def logout_page(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        # TODO: maybe return to last visited page???7?
        return HttpResponseRedirect('/')
