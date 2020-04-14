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
    print(request)
    # return render(request, 'base.html')
    # if request.GET.get('guest'):
    user = authenticate(username='guest', password='dickerydick')
    login(request, user)
    print(user)
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
