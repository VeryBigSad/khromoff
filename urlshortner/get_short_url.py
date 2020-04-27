import string
from datetime import datetime

from django.core.exceptions import PermissionDenied

from .models import ShortUrl

import random
import re

from khromoff.exceptions import *
from urlshortner.constants import MAX_URL_LENGTH, MAX_SHORTCODE_LENGTH


def get_shorturl(thing_object, url_length, filter_kwargs=None, check_for_existing_var=None):
    # generates unique (or not, if check_for_existing == False) character-set of length [url_length] with
    # alphabet [alphabet]. Checks if unique or not in thing_object.objects class

    if filter_kwargs is None:
        filter_kwargs = {}
    alphabet = 'abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789-'

    unique = False
    short_code = ''
    max_tries = 2  # How much requests to database, till we will give up on url_length and add 1 symbol to it
    tries = 0
    while not unique:
        tries += 1
        short_code = ''.join([random.choice(alphabet) for i in range(url_length)])
        if check_for_existing_var:
            filter_kwargs.update({check_for_existing_var: short_code})
        if not thing_object.objects.filter(**filter_kwargs).exists():
            unique = True
        if tries > max_tries:
            url_length += 1
            tries = 0

    return short_code


def return_real_url(url):
    # tries to make actual URL out of what crap user gave us, or raises exception

    if not ('http://' in url or 'https://' in url):
        url = 'https://' + url
    # TODO: check url on recursive redirecting

    if ' ' in url or not '.' in url:
        raise InvalidUrlError
    if len(url) > MAX_URL_LENGTH:
        raise InvalidUrlError

    if re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        return url
    else:
        raise InvalidUrlError


def get(long_url, request, url_length=3):
    # If possible, creates short url of length url_length
    # If not (2 [max_tries] tries of random pick - means that it is impossible)
    # So, if not, creates url_length + 1. And so on until it creates it.

    long_url = return_real_url(long_url)

    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') is not None else False)()
    # We don't need to generate shorturl if we are provided by it.

    if do_collect_meta and request.user.is_anonymous:
        # you have to be logged in to do that.
        raise PermissionDenied

    if request.POST.get('alias'):
        # TODO: make it so everyone can make an alias
        # TODO: DO_COLLECT_META = False by default

        if ShortUrl.objects.filter(short_code=request.POST['alias'].lower()).exists():
            raise NameExistsError

        if 3 > len(request.POST['alias']) or len(request.POST['alias']) > MAX_SHORTCODE_LENGTH:
            raise InvalidAliasError

        for i in request.POST['alias'].lower():
            if i not in string.ascii_lowercase + '0123456789-_':
                raise InvalidAliasError

        return register(request.POST['alias'].lower(), request, long_url)

    # if we already registred this url, we authorize it.
    obj = ShortUrl.objects.filter(full_url=long_url, alias=False, do_collect_meta=do_collect_meta)
    if obj.exists() and len(obj[0].short_code) == url_length and not do_collect_meta:
        obj = obj[0]

        obj.pk = None
        obj.time_created = datetime.today()
        if do_collect_meta:
            obj.view_data_code = get_shorturl(ShortUrl, 30, check_for_existing_var='view_data_code')

            # TODO: key check here
            # if request.POST['key']:
            #     obj.key = request.POST['key']
            if request.user.is_authenticated:
                obj.author = request.user

        obj.save()  # updating time it was created, because yes.

        return obj

    short_code = get_shorturl(ShortUrl, url_length, filter_kwargs={}, check_for_existing_var='short_code')

    obj = register(short_code, request, long_url)
    return obj


# Creates entry in DB
def register(short_code, request, long_url, key=None):
    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') else False)()
    alias = (lambda: False if request.POST['alias'] == '' else True)()

    new_obj = ShortUrl(
        short_code=short_code, do_collect_meta=do_collect_meta,
        full_url=long_url, creator_ip=request.META['REMOTE_ADDR'],
        alias=alias
    )
    if do_collect_meta:
        new_obj.view_data_code = get_shorturl(ShortUrl, 30, check_for_existing_var='view_data_code')
        if key:
            new_obj.key = key
        elif request.user.is_authenticated:
            new_obj.author = request.user

    # also possible that no auth data sent.

    new_obj.save()
    return new_obj
