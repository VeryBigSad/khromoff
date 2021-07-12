from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import IntegerField

from api.models import UserAPIKey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserAPIKeySerializer(serializers.ModelSerializer):
    requests_per_minute = IntegerField(
        max_value=30
    )

    def create(self, validated_data, *args, **kwargs):
        return self.Meta.model.objects.create_key(**validated_data)

    def deactivate(self):
        self.active = False

    class Meta:
        model = UserAPIKey
        fields = '__all__'
