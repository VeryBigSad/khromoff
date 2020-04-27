from django.core.exceptions import PermissionDenied
from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from khromoff import settings
from urlshortner.models import ShortUrl, Visit

from khromoff.exceptions import NameExistsError, InvalidAliasError, InvalidUrlError
from .get_short_url import get


def create_new_link(request):
    if request.method == 'POST':

        # if we are getting short url to ourselves
        errors = []
        try:
            short_obj = get(request.POST['long_url'], request=request)
            short_code = short_obj.short_code
        except NameExistsError:
            errors.append({'type': 'invalid_alias',
                           'description': 'This alias already exists, try another or random.'})

        # TODO: replace this with rest exception
        except PermissionDenied:
            errors.append({'type': 'permission_denied',
                           'description': 'You don\'t have enough permissions to do that.'})
        except InvalidAliasError:
            errors.append({'type': 'alias_too_short',
                           'description': 'Please, use alias from 3 to 30 symbols length, '
                                          'and only letters, numbers, and underscore.'})
        except InvalidUrlError:
            errors.append({'type': 'invalid_url',
                           'description': 'URL you passed is either invalid or '
                                          'links to this site. Please check the correctness.'})

        if errors:
            return render(request, 'new_shorten_url_form.html', context={'errors': errors})

        url = reverse('urlshortner:preview', kwargs={'short_id': short_code})
        if short_obj.view_data_code:
            url += '?view_data_code=' + short_obj.view_data_code

        return redirect(url)

    else:
        return render(request, 'new_shorten_url_form.html', context={})


def view_data(request, view_data_code):
    shorturl = get_object_or_404(ShortUrl, view_data_code=view_data_code)

    return render(request, 'view_data.html', context={
        'shorturl': shorturl, 'visits': Visit.objects.filter(shorturl=shorturl)})


def redirect_to_long_url(request, short_id):
    url_object = ShortUrl.objects.filter(short_code=short_id)
    if not url_object.exists():
        url_object = ShortUrl.objects.filter(short_code=short_id.lower(), alias=True)
        if not url_object.exists():
            raise Http404('We are unable to find this shorturl.'
                          ' Please check that url is entered'
                          ' correctly.')
    url_object = url_object[0]
    long_url = url_object.full_url

    if url_object.do_collect_meta:
        meta_obj = Visit(shorturl=url_object, IP=request.META['REMOTE_ADDR'],
                         user_agent=request.META['HTTP_USER_AGENT'], http_referer=request.META.get('HTTP_REFERER'))
        meta_obj.save()

    return redirect(long_url)


def preview(request, short_id):
    obj = get_object_or_404(ShortUrl, short_code=short_id)

    # TODO: send view_data_code var only if author created it.
    return render(request, 'preview.html', context={'long_url': obj.full_url, 'do_collect_meta': obj.do_collect_meta,
                                                    'short_code': short_id, 'view_data_code': obj.view_data_code})
