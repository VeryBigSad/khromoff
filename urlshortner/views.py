from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponseRedirect, Http404
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
            short_code = get(request.POST['long_url'], request=request)
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

        if not request.POST.get('do_collect_meta') and request.user.is_authenticated:
            url = reverse('shorturl-a-p-redirect', kwargs={'short_id': short_code})
        else:
            url = reverse('shorturl-p-redirect', kwargs={'short_id': short_code})
        return HttpResponseRedirect(url)
    else:
        return render(request, 'new_shorten_url_form.html', context={})


@login_required()
def view_data(request, view_data_code):
    shorturl = ShortUrl.objects.filter(view_data_code=view_data_code)
    if shorturl.exists():
        return render(request, 'view_data.html', context={'shorturl': shorturl[0],
                      'visits': Visit.objects.filter(shorturl=shorturl[0])})
    else:
        raise Http404


def redirect(request, short_id, preview=False, anonymous=False):
    url_object = ShortUrl.objects.filter(short_code=short_id, do_collect_meta=not anonymous)
    if not url_object.exists():
        url_object = ShortUrl.objects.filter(short_code=short_id.lower(), do_collect_meta=not anonymous, alias=True)
        if not url_object.exists():
            return render(request, '404error.html', context={'description': 'We are unable to find this shorturl.'
                                                                            ' Please check that url is entered'
                                                                            ' correctly.'}, status=404)
            # raise Http404
    print(url_object)
    url_object = url_object[0]
    long_url = url_object.full_url

    if url_object.do_collect_meta:
        meta_obj = Visit(shorturl=url_object, IP=request.META['REMOTE_ADDR'],
                         user_agent=request.META['HTTP_USER_AGENT'], http_referer=request.META.get('HTTP_REFERER'))
        meta_obj.save()

    if preview:
        return render(request, 'preview.html', context={'long_url': long_url, 'do_collect_meta': anonymous,
                                                        'short_code': short_id})

    return HttpResponseRedirect(long_url)
