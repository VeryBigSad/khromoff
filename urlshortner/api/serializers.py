from rest_framework import serializers

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from urlshortner.api.permissions import IsShortURLOwner, IsVisitOwner
from urlshortner.models import ShortUrl, Visit


class BasicShortUrlSerializer(serializers.ModelSerializer):
    """
        Serializer for ShortURL class
    """

    permission_classes = [AllowAny]

    class Meta:
        model = ShortUrl
        read_only_fields = ['short_code', 'full_url', 'do_collect_meta', 'alias']


class FullShorturlSerializer(serializers.ModelSerializer):
    """
        Same as Basic, but all fields are available.
    """
    permission_classes = [HasAPIKey & IsShortURLOwner | IsAuthenticated & IsShortURLOwner]

    class Meta:
        model = ShortUrl
        fields = ['active']
        read_only_fields = ['short_code', 'full_url', 'do_collect_meta', 'alias', 'key', 'author', 'view_data_code',
                            'creator_ip', 'time_created']


class VisitSerializer(serializers.ModelSerializer):
    permission_classes = [HasAPIKey & IsVisitOwner | IsVisitOwner & IsAuthenticated]

    class Meta:
        model = Visit
        read_only_fields = ['shorturl', 'http_referer', 'time', 'user-agent', 'IP']
