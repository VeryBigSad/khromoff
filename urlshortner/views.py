from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django_hosts import reverse

from urlshortner.api.serializers import ShorturlSerializer
from urlshortner.constants import MAX_SHORTCODE_LENGTH
from urlshortner.models import ShortUrl, Visit


def create_new_link(request):
    if request.method == 'POST':

        # if we are getting short url to ourselves
        errors = []
        data = {'full_url': request.POST.get('full_url')}
        if request.POST.get('do_collect_meta'):
            data.update({'do_collect_meta': True})
        if request.POST.get('short_code'):
            data.update({'short_code': request.POST['short_code']})

        # most people dont type in http(s)://, so that will do it for them (before checks)
        try:
            if data['full_url'][:4] != 'http':
                data['full_url'] = 'https://' + data['full_url']
        except TypeError:
            # None[:4] is an error
            pass

        short_obj = ShorturlSerializer(data=data, context={'request': request})
        # TODO: make it so it will make a http request through AJAX
        if short_obj.is_valid():
            short_obj.save()
            short_code = short_obj.data['short_code']
        else:
            for err, desc in short_obj.errors.items():
                errors.append({'code': desc[0].code,
                               'field': err,
                               'description': desc[0]})
                # TODO: add in template, if code == 'input_name', add is_invalid class to input tag.
            return render(request, 'urlshortner/new_shorten_url_form.html',
                          context={'errors': errors,
                                   'post': request.POST,
                                   'max_length': MAX_SHORTCODE_LENGTH}
                          )
        url = reverse('preview', kwargs={'short_id': short_code}, host='urlshortner')
        if short_obj.data['do_collect_meta']:
            url += '?view_data_code=' + short_obj.data['view_data_code']

        return redirect(url)

    else:
        return render(request, 'urlshortner/new_shorten_url_form.html', context={'max_length': MAX_SHORTCODE_LENGTH})


def view_data(request, view_data_code):
    shorturl = get_object_or_404(ShortUrl, view_data_code=view_data_code)
    visits = Visit.objects.filter(shorturl=shorturl)
    visits.reverse()

    return render(request, 'urlshortner/view_data.html', context={
        'shorturl': shorturl, 'visits': visits})


@cache_page(60 * 15)
def redirect_to_long_url(request, short_id):
    url_base_obj = ShortUrl.objects.get_valid_urls()
    url_object = url_base_obj.filter(short_code=short_id)
    if not url_object.exists():
        url_object = url_base_obj.filter(short_code=short_id.lower(), alias=True)
        if not url_object.exists():
            raise Http404('We are unable to find this shorturl.'
                          ' Please check that url is entered'
                          ' correctly.')
    url_object = url_object[0]
    if not url_object.active:
        raise Http404('This URL is blocked by site owners or ShortURL author.')
    long_url = url_object.full_url

    if url_object.do_collect_meta:
        meta_obj = Visit(shorturl=url_object, IP=request.META['REMOTE_ADDR'],
                         user_agent=request.META['HTTP_USER_AGENT'], http_referer=request.META.get('HTTP_REFERER'))
        meta_obj.save()

    return redirect(long_url)


def preview(request, short_id):
    try:
        obj = get_object_or_404(ShortUrl, short_code=short_id, do_collect_meta=False)
    except Http404:
        obj = get_object_or_404(ShortUrl, short_code=short_id)

    return render(request, 'urlshortner/preview.html',
                  context={'long_url': obj.full_url, 'do_collect_meta': obj.do_collect_meta,
                           'short_code': short_id})


def about(request):
    return render(request, 'urlshortner/about.html')
