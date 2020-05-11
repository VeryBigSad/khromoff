from django.shortcuts import render, Http404, redirect, get_object_or_404
from django_hosts import reverse

from urlshortner.api.serializers import ShorturlSerializer
from urlshortner.constants import MAX_URL_LENGTH, MAX_SHORTCODE_LENGTH
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

        # most people dont type in http://, so that will do it for them (before checks)
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
            error_codes = {'Enter a valid URL.': 'Это не настоящая ссылка, проверьте правильность написания.',
                           'URL can\'t redirect to this same site': 'Ссылка не может указывать на этот сайт.',
                           'URL is too long (%s symbols max)' % MAX_URL_LENGTH:
                               'Ссылка слишком длинная, макс. длина - %s символов.' % MAX_URL_LENGTH,
                           'This Alias is already taken.': 'Эта короткая ссылка уже занята, выберите другую.',
                           'Alias must have length from 4 to %s symbols.' % MAX_SHORTCODE_LENGTH:
                               'Короткая ссылка должна быть длинной от 4 до %s символов.' % MAX_SHORTCODE_LENGTH,
                           'Only letters, numbers, and underscores in alias': 'Только латинские буквы, цифры, '
                                                                              'и нижние подчеркивания в короткой '
                                                                              'ссылке.',
                           }
            for err, desc in short_obj.errors.items():
                errors.append({'code': desc[0].code,
                               'field': err,
                               'description': error_codes[str(desc[0])]})
            return render(request, 'urlshortner/new_shorten_url_form.html', context={'errors': errors,
                                                                                     'post': request.POST})
        url = reverse('preview', kwargs={'short_id': short_code}, host='urlshortner')
        if short_obj.data['do_collect_meta']:
            url += '?view_data_code=' + short_obj.data['view_data_code']

        return redirect(url)

    else:
        return render(request, 'urlshortner/new_shorten_url_form.html', context={})


def view_data(request, view_data_code):
    shorturl = get_object_or_404(ShortUrl, view_data_code=view_data_code)

    return render(request, 'urlshortner/view_data.html', context={
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
    try:
        obj = get_object_or_404(ShortUrl, short_code=short_id, do_collect_meta=False)
    except Http404:
        obj = get_object_or_404(ShortUrl, short_code=short_id)

    return render(request, 'urlshortner/preview.html',
                  context={'long_url': obj.full_url, 'do_collect_meta': obj.do_collect_meta,
                           'short_code': short_id})


def about(request):
    return render(request, 'urlshortner/about.html')
