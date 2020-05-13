from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.http import HttpResponse
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.views import APIView

from api.utils import ParamRequired
from api.utils import Response
from urlshortner.api.permissions import DoCollectMetaPermission, IsVisitOwner, IsShorturlOwner
from urlshortner.api.serializers import ShorturlSerializer, VisitSerializer
from urlshortner.models import ShortUrl, Visit


class ShorturlDetails(APIView):
    http_method_names = ['get', 'post']

    def get(self, request):
        if request.method == 'GET':
            short_code = request.GET.get('short_code')
        else:
            short_code = request.POST.get('short_code')

        try:
            shorturl = ShortUrl.objects.get(short_code=short_code)
        except ShortUrl.DoesNotExist:
            raise Http404

        serializer = ShorturlSerializer(shorturl, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return self.get(request)


class CreateShorturl(APIView):
    http_method_names = ['get', 'post']
    permission_classes = [DoCollectMetaPermission]

    def get(self, request):
        if request.method == 'GET':
            data = request.GET
        else:
            data = request.POST

        serializer = ShorturlSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        return self.get(request)


class VisitDetails(APIView):
    """
        Details for listing or retrieving Visits.
    """

    permission_classes = [IsVisitOwner]
    serializer_class = VisitSerializer
    http_method_names = ['get', 'post']
    queryset = Visit.objects.all()

    def get_data(self):

        if len(self.request.data) == 0:
            data = dict()

            for METHOD_NAME in self.http_method_names:
                if self.request.method == METHOD_NAME.upper():
                    data.update(self.request.__getattr__(METHOD_NAME.upper()))
            for i in data:
                data[i] = data[i][0]

            return data
        else:
            return self.request.data

    def get(self, request):
        data = self.get_data()
        pk = data.get('id')
        short_code = data.get('short_code')
        required_params = ['short_code']

        for i in required_params:
            if i not in data:
                raise ParamRequired('Parameter %s was required but wasn\'t specified' % i)

        if pk:
            # one specified visit
            # TODO: not get_object, but rather use serializer here.
            visit = get_object_or_404(self.queryset, id=pk, shorturl__short_code=short_code)
            self.check_object_permissions(request, visit)
            serializer = VisitSerializer(visit, context={'request': request})
            count = 1
        else:
            # visit list
            visits = self.queryset.filter(shorturl__short_code=short_code)

            try:
                # Note: every single one of visits has 1 single owner,
                # and since there is only 1 permission check (assigned to owner),
                # we can check it and forget about the rest (because result would be the same)
                self.check_object_permissions(request, visits[0])
            except IndexError:
                # this means visits QuerySet is empty.
                # checking if ShortURL exists in the first place...
                if not ShortUrl.objects.filter(short_code=short_code).exists():
                    raise Http404

            serializer = VisitSerializer(visits, many=True, context={'request': request})
            count = len(serializer.data)

        return Response({'count': count, 'visits': serializer.data})

    def post(self, request):
        return self.get(request)


class ShorturlDeactivate(APIView):
    permission_classes = [IsShorturlOwner]
    serializer_class = ShorturlSerializer
    http_method_names = ['get', 'post', 'options']
    queryset = ShortUrl.objects.all()
    required_params = ['short_code']

    def options(self, request, *args, **kwargs):
        resp = HttpResponse()
        # ajax will never calm down so here i am writing VERY bad code,
        # probably a lot simpler solution exists. This works though
        resp['Access-Control-Allow-Credentials'] = 'true'
        resp['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
        resp["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, access-control-allow-origin, Origin," \
                                               "Accept, X-Requested-With, " \
                                               "Content-Type, Access-Control-Request-Method, " \
                                               "Access-Control-Request-Headers "

        return resp

    def get(self, request):
        if request.method == 'POST':
            data = request.POST
            try:
                if request.POST['headers[X-Requested-With]'] == 'XMLHttpRequest':
                    # same as .is_ajax() but i can't do things right so yes
                    data_tmp = data['data'].split('&')
                    data = {}
                    for i in data_tmp:
                        i = i.split('=')
                        data[i[0]] = i[1]
                else:
                    raise AttributeError
            except AttributeError:
                data = request.POST

        else:
            # GET method; elif request.method == 'GET':
            data = request.GET

        for i in self.required_params:
            if i not in data:
                raise ParamRequired('Parameter %s was required but wasn\'t specified' % i)

        shorturl = get_object_or_404(self.queryset, short_code=data.get('short_code'))
        self.check_object_permissions(request, shorturl)

        shorturl.deactivate()
        shorturl.save()

        # deleting cache of /profile shorturls-list (because some of it is invalid now)
        key = make_template_fragment_key('shorturl-profile-list', [request.user.username])
        cache.delete(key)

        # TODO: exception on accessing Inactive data
        return Response(self.serializer_class(shorturl, context={'request': request}).data)

    def post(self, request):
        return self.get(request)
