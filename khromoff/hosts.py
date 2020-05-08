from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
                         host('', settings.ROOT_URLCONF, name='index'),

                         host('l', 'urlshortner.urls', name='urlshortner'),
                         host('api', 'api.urls', name='api')
                         )
