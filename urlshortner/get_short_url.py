from .models import ShortUrl
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import PermissionDenied
import random


def get(long_url, request, url_length=3, do_register=True):
    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') is not None else False)()

    # We don't need to generate it if we are provided by it.
    if request.POST.get('alias') and request.user == AnonymousUser:
        obj = ShortUrl.objects.filter(long_url=None, short_code=request.POST.get('alias'))
        if long_url and obj.exists():
            obj.long_url = request.POST['long_url']
            obj.save()
            return request.POST.get('alias')
        if do_register:
            raise PermissionDenied

    elif request.user != AnonymousUser and request.POST.get('alias'):
        if ShortUrl.objects.filter(short_code=request.POST['alias']).exists():
            # TODO: NameError is when something doesn't exist, in our case problem that such alias exists already.
            raise NameError

        if len(request.POST['alias']) < 3:
            # TODO: Overflow error is not for this but whatever
            raise OverflowError

        register(request.POST['alias'], request)
        return request.POST['alias']

    obj = ShortUrl.objects.filter(full_url=long_url, alias=False, do_collect_meta=do_collect_meta)
    if obj.exists() and len(obj[0].short_code) == url_length:
        short_code = obj[0].short_code
        return short_code

    alphabet = 'abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789-'

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

    register(short_code, request)
    return short_code


def register(short_code, request):
    do_collect_meta = (lambda: True if request.POST.get('do_collect_meta') is not None else False)()
    alias = (lambda: True if request.POST.get('alias') else False)()

    new_obj = ShortUrl(short_code=short_code, do_collect_meta=do_collect_meta,
                       full_url=request.POST.get('long_url'), creator_ip=request.META['REMOTE_ADDR'],
                       alias=alias)
    if request.user.is_authenticated:
        new_obj.author = request.user
    new_obj.save()
