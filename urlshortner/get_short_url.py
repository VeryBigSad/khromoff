from .models import ShortUrl
from django.contrib.auth.models import PermissionDenied

import random
from urllib.parse import urlparse

from khromoff.exceptions import *


def return_real_url(url):
    # TODO: IMPORTANT! FINISH!
    if not ('https://' in url or 'http://' in url) and '://' not in url:
        url = 'https://' + url
        if '.' not in url:
            raise InvalidUrlError
    else:
        raise InvalidUrlError

    return url


def get(long_url, request, url_length=3):
    # If possible, creates short url of length url_length
    # If not (2 [max_tries] tries of random pick - means that it is impossible)
    # So, if not, creates url_length + 1. And so on until it creates it.

    long_url = return_real_url(long_url)

    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') is not None else False)()

    # We don't need to generate it if we are provided by it.
    if request.POST.get('alias') and request.POST.get('alias') != 'Only for authorised users':
        if request.user.is_anonymous:
            raise PermissionDenied

        if ShortUrl.objects.filter(short_code=request.POST['alias']).exists():
            raise NameExistsError

        if len(request.POST['alias']) < 3:
            raise InvalidAliasError

        register(request.POST['alias'], request, long_url)
        return request.POST['alias']

    # if we already registred this url, we authorize it.
    obj = ShortUrl.objects.filter(full_url=long_url, alias=False, do_collect_meta=do_collect_meta)
    if obj.exists() and len(obj[0].short_code) == url_length:
        short_code = obj[0].short_code
        return short_code

    alphabet = 'abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789-_'

    unique = False
    short_code = ''
    max_tries = 2  # How much requests to database, till we will give up on url_length and add 1 symbol to it
    tries = 0
    while not unique:  # TODO: use a/<short_code>, so for anonymous and not there's two different things
        tries += 1
        short_code = ''.join([random.choice(alphabet) for i in range(url_length)])
        if not ShortUrl.objects.filter(short_code=short_code, do_collect_meta=do_collect_meta).exists():
            unique = True
        if tries > max_tries:
            url_length += 1
            tries = 0

    register(short_code, request, long_url)
    return short_code


# Creates entry in DB
def register(short_code, request, long_url=None):
    if long_url is None:
        long_url = request.POST['long_url']

    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') is not None or
                                       request.user.is_anonymous else False)()
    alias = (lambda: False if request.POST['alias'] == '' else True)()

    new_obj = ShortUrl(short_code=short_code, do_collect_meta=do_collect_meta,
                       full_url=long_url, creator_ip=request.META['REMOTE_ADDR'],
                       alias=alias)
    if request.user.is_authenticated:
        new_obj.author = request.user
    new_obj.save()
