from django.contrib import admin

from .models import ShortUrl, Visit

admin.site.register(ShortUrl)
admin.site.register(Visit)

