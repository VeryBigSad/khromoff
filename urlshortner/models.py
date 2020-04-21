from django.db import models
from django.contrib.auth.models import User

from urlshortner.settings import MAX_SHORTCODE_LENGTH, MAX_URL_LENGTH


class ShortUrl(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    creator_ip = models.GenericIPAddressField(default='127.0.0.1')
    time_created = models.DateTimeField(auto_now=True)

    do_collect_meta = models.BooleanField(default=True)

    active = models.BooleanField(default=True)
    alias = models.BooleanField(default=False)
    short_code = models.CharField(max_length=MAX_SHORTCODE_LENGTH)
    full_url = models.URLField(max_length=MAX_URL_LENGTH, null=True)

    def __str__(self):
        return str(self.full_url)


class Visit(models.Model):
    shorturl = models.ForeignKey(ShortUrl, on_delete=models.CASCADE)

    http_referer = models.CharField(default=None, null=True, max_length=999)
    time = models.DateTimeField(auto_now=True)
    user_agent = models.CharField(max_length=999)
    IP = models.GenericIPAddressField(default='127.0.0.1')

    def __str__(self):
        return self.time.strftime("%A, %d. %B %Y %H:%M:%S")
