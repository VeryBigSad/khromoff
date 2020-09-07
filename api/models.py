from django.contrib.auth import get_user_model
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

User = get_user_model()


class UserAPIKey(AbstractAPIKey):
    is_super_key = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # who owns the key
    requests_per_minute = models.IntegerField(default=30)  # throttle value

    def deactivate(self):
        self.revoked = True
