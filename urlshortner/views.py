from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from khromoff import settings
from urlshortner.models import ShortUrl, Visit

from khromoff.exceptions import NameExistsError, InvalidAliasError, InvalidUrlError
from .get_short_url import get


def create_new_link(request):
    if request.method == 'POST':

        # if we are getting short url to ourselves
        if '://' + settings.HOSTNAME + '/s' in request.POST['long_url']:
            return render(request, 'new_shorten_url_form.html', context={
                'errors': [{'type': 'this_site_link', 'description': 'This URL links to other short url. '
                                                                     'You can\'t do that!'}],
                'form_fields': {'long_url': request.POST['long_url']}, 'old': dict(request.POST)})
        try:
            short_code = get(request.POST['long_url'], request=request)
        except NameExistsError:
            return render(request, 'new_shorten_url_form.html',
                          context={'errors': [{'type': 'invalid_alias',
                                               'description': 'This alias already exists, try another or random.'}]})
        except PermissionDenied:
            return render(request, 'new_shorten_url_form.html',
                          context={'errors': [{'type': 'permission_denied',
                                               'description': 'You don\'t have enough permissions to do that.'}]})
        except InvalidAliasError:
            return render(request, 'new_shorten_url_form.html',
                          context={'errors': [{'type': 'alias_too_short',
                                               'description': 'You can\'t use such a small alias, only 3+ symbols.'}]})
        except InvalidUrlError:
            return render(request, 'new_shorten_url_form.html',
                          context={'errors': [{'type': 'invalid_url',
                                               'description': 'URL you passed in is invalid, maybe a typo?'}]})
        url = '/shorturl/p/' + short_code + '?new=1'
        if not request.POST.get('do_collect_meta') and request.user.is_authenticated:
            url = '/shorturl/a/p/' + short_code + '?new=1'
        return HttpResponseRedirect(url)
    else:
        return render(request, 'new_shorten_url_form.html', context={})


@login_required()
def links(request):
    return render(request, 'links.html', context={'links': ShortUrl.objects.filter(author=request.user)})


def redirect(request, short_id, preview=False, anonymous=False):
    url_object = ShortUrl.objects.filter(short_code=short_id, do_collect_meta=not anonymous)
    if url_object.exists():
        url_object = url_object[0]
        long_url = url_object.full_url

        if url_object.do_collect_meta:
            meta_obj = Visit(shorturl=url_object, IP=request.META['REMOTE_ADDR'],
                             user_agent=request.META['HTTP_USER_AGENT'])
            meta_obj.save()

        if preview:
            return render(request, 'preview.html', context={'long_url': long_url, 'do_collect_meta': anonymous,
                                                            'short_code': short_id})

        return HttpResponseRedirect(long_url)

    else:
        raise Http404


