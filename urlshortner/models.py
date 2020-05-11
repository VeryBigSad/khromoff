from django.contrib.auth import get_user_model
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

from api.models import UserAPIKey
from urlshortner.constants import MAX_SHORTCODE_LENGTH, MAX_URL_LENGTH

User = get_user_model()


class ShortUrl(models.Model):
    # key - key with which url was created
    key = models.ForeignKey(UserAPIKey, on_delete=models.SET_DEFAULT, default=None, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    active = models.BooleanField(default=True)

    creator_ip = models.GenericIPAddressField(default='127.0.0.1')
    time_created = models.DateTimeField(auto_now=True)

    full_url = models.CharField(max_length=MAX_URL_LENGTH)
    short_code = models.CharField(max_length=MAX_SHORTCODE_LENGTH, unique=True)
    do_collect_meta = models.BooleanField(default=True)
    alias = models.BooleanField(default=False)
    # page where we can see spy info actually
    view_data_code = models.CharField(max_length=MAX_SHORTCODE_LENGTH + 1, default=None, null=True)

    def __str__(self):
        return str(self.time_created.strftime("%d.%m.%Y %H:%M:%S; ") + self.full_url)


class Visit(models.Model):
    shorturl = models.ForeignKey(ShortUrl, on_delete=models.CASCADE)

    http_referer = models.CharField(default=None, null=True, max_length=999)
    time = models.DateTimeField(auto_now=True)
    user_agent = models.CharField(max_length=999)
    IP = models.GenericIPAddressField(default='127.0.0.1')

    def __str__(self):
        return str(self.time.strftime("%d.%m.%Y %H:%M:%S; ")) + self.IP + '; ' + self.shorturl.full_url
