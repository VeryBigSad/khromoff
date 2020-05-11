from django.db import models


class BugReport(models.Model):
    time = models.DateTimeField(auto_created=True)
    ip = models.GenericIPAddressField()
    description = models.CharField(max_length=500, default='', blank=True)
    view_name = models.CharField(max_length=50)
    request_obj = ''
    status_code = models.IntegerField()
    data = ''
