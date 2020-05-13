# in this file because in utils.py it causes circular import error
from logging import getLogger

from django.http import Http404
from rest_framework.views import exception_handler

logger = getLogger('khrmff.api')


def api_exception_handler(exc, context):
    logger.warning('API Exception: context: %s exc_type: %s' % (str(context), type(exc)))

    # TODO: make it work not this shit
    # NO_AUTH_ERROR_CODE = 1

    request = context['request']
    response = exception_handler(exc, context)
    errors = {
        'ITEM_NOT_FOUND_ERROR': {
            'code': 'item_not_found',
            'desc': 'Item filtered by your query wasn\'t found.'
        },
        'not_authenticated': {
            'code': 'not_authenticated',
            'desc': 'Required credentials were not provided.'
        }
    }

    if response is not None:
        response.data['error'] = response.data['detail']
        del response.data['detail']
        try:
            try:
                response.data['error'] = {'error_code': errors[exc.default_code]['code'],
                                          'description': errors[exc.default_code]['desc']}
            except KeyError:
                response.data['error'] = {'error_code': exc.default_code,
                                          'description': exc.detail}
        except AttributeError:
            if type(exc) == Http404:
                response.data['error'] = {'error_code': errors['ITEM_NOT_FOUND_ERROR']['code'],
                                          'description': errors['ITEM_NOT_FOUND_ERROR']['desc']}

        kwargs = dict(request.POST)
        kwargs.update(dict(request.GET))
        for key, val in kwargs.items():
            kwargs[key] = val[0]
        response.data['error']['kwargs'] = kwargs
    return response
