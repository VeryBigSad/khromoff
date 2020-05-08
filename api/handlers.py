# in this file because in utils.py it causes circular import error
from django.http import Http404
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    # # TODO: add all errors into file or something
    # NO_AUTH_ERROR_CODE = 1

    response = exception_handler(exc, context)
    errors = {
        'ITEM_NOT_FOUND_ERROR': {
            'code': 404,
            'desc': 'Item filtered by your query wasn\'t found.'
        }
    }

    if response is not None:
        response.data['error'] = response.data['detail']
        del response.data['detail']
        try:
            response.data['error'] = {'error_code': exc.default_code,
                                      'description': exc.detail}
        except AttributeError:
            if type(exc) == Http404:
                response.data['error'] = {'error_code': errors['ITEM_NOT_FOUND_ERROR']['code'],
                                          'description': errors['ITEM_NOT_FOUND_ERROR']['desc']}
    return response
