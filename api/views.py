import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from api.models import UserAPIKey
from api.serializers import UserAPIKeySerializer


def methods(request):
    return render(request, 'docs/api_methods.html', context={})


def make_request(request):
    if request.method == 'POST':
        post = request.POST
        data = {
            post['var1']: post['var1_val'],
            post['var2']: post['var2_val'],
            post['var3']: post['var3_val'],
        }

        r = requests.post('https://khrmff.online/' + request.POST['url'], data={**data}, verify=False)
        try:
            return render(request, 'make_request.html', context={'resp': r.json()})
        except:
            return render(request, 'make_request.html', context={'resp': r.text})
    else:
        return render(request, 'make_request.html')


def quickstart(request):
    return render(request, 'docs/api_quickstart.html')


def objects(request):
    return render(request, 'docs/api_objects.html')


def errors(request):
    return render(request, 'docs/api_errors.html')


@login_required()
def create_key(request):
    if request.method == 'POST':
        if UserAPIKey.objects.filter(user=request.user).count() >= 5:
            return render(request, 'keys/max_key_amount.html')

        data = {'user': request.user.pk, 'name': request.POST.get('name'),
                'requests_per_minute': int(request.POST.get('requests_per_minute'))}

        serializer = UserAPIKeySerializer(data=data)
        if serializer.is_valid():
            key = serializer.save()
            return render(request, 'keys/key_created.html', context={'raw_api_key': key[1]})
        else:
            return render(request, 'keys/create_key.html', context={'errors': serializer.errors})

    elif request.method == 'GET':
        if UserAPIKey.objects.filter(user=request.user).count() >= 5:
            return render(request, 'keys/max_key_amount.html')
        return render(request, 'keys/create_key.html', context={})


def redirect_to_docs(request):
    return redirect('docs-index')


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def user_details(request):
    return JsonResponse({'not_finished_yet': True})
