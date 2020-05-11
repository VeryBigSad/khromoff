from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import ParamRequired
from urlshortner.api.permissions import DoCollectMetaPermission, IsVisitOwner
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
            return Response(status=404)

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
            visit = get_object_or_404(self.queryset, id=pk, shorturl__short_code=short_code)
            self.check_object_permissions(request, visit)
            serializer = VisitSerializer(visit, context={'request': request})
            count = 1
        else:
            # visit list
            visits = self.queryset.filter(shorturl__short_code=short_code)
            try:
                self.check_object_permissions(request, visits[0])
                # Note: every single one of visits has 1 single owner,
                # and since there is only 1 permission check (assigned to owner),
                # we can check it and forget about the rest (because result would be the same)
            except IndexError:
                # visits QuerySet is empty.
                pass

            if not visits.exists():
                raise Http404()

            serializer = VisitSerializer(visits, many=True, context={'request': request})
            count = len(serializer.data)

        return Response({'count': count, 'response': serializer.data})

    def post(self, request):
        return self.get(request)