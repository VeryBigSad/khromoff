from django.shortcuts import render


def error404(request, exception):
    return render(request, '404error.html', status=404)


def error500(request):
    return render(request, '500error.html', status=500)
