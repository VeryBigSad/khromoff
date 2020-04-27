from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView

from urlshortner.api.permissions import IsVisitOwner, IsShortURLOwner
from urlshortner.models import ShortUrl
from urlshortner.api.serializers import BasicShortUrlSerializer, FullShorturlSerializer, VisitSerializer


@api_view(['GET', 'POST'])
def shorturl_details(request):
    # if
    # permissions stuff

    try:
        pk = request.POST['pk']
    except KeyError:
        try:
            pk = request.GET['pk']
        except KeyError:
            # TODO: error, param not specified
            pass

    try:
        shorturl = ShortUrl.objects.get(pk=pk)
    except ShortUrl.DoesNotExist:
        return HttpResponse(status=404)

    serializer = shorturl
    return JsonResponse(serializer.data)


def get(self, request, pk):
    pk = request.GET['pk']
    # TODO: if 'detailed', check on permissions, and then

    try:
        shorturl = ShortUrl.objects.get(pk=pk)
    except ShortUrl.DoesNotExist:
        return HttpResponse(status=404)

    serializer = self.get_serializer_class()(shorturl)
    return JsonResponse(serializer.data)


def visit_details(self, request):
    pk = request.POST['pk']
    # TODO: if 'detailed', check on permissions, and then

    try:
        shorturl = ShortUrl.objects.get(pk=pk)
    except ShortUrl.DoesNotExist:
        return HttpResponse(status=404)

    serializer = self.get_serializer_class()(shorturl)
    return JsonResponse(serializer.data)
