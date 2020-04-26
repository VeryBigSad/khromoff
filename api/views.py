import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'docs_index.html', context={})
    # return HttpResponseRedirect(reverse('api-make-request'))


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
