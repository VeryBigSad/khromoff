import datetime
import string
from logging import getLogger

from rest_framework import serializers
from rest_framework.fields import CharField, URLField, DateTimeField
from rest_framework.permissions import AllowAny
from rest_framework.relations import StringRelatedField, SlugRelatedField
from rest_framework.validators import UniqueValidator

from khromoff.settings import DOMAIN_NAME
from urlshortner.api.permissions import IsVisitOwner
from urlshortner.constants import SHORTCODE_BASE_LENGTH, MAX_SHORTCODE_LENGTH, MAX_URL_LENGTH, MIN_SHORTCODE_LENGTH
from urlshortner.models import ShortUrl, Visit
from urlshortner.utils import get_shorturl

logger = getLogger('khromoff.api')


class ShorturlSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]

    full_url = URLField(
        required=True,
    )
    short_code = CharField(
        validators=[UniqueValidator(queryset=ShortUrl.objects.all())],
        required=False
    )
    time_created = DateTimeField(
        format='%d.%m.%Y %H:%M:%S',
        read_only=True
    )
    key = SlugRelatedField(
        slug_field='prefix',
        read_only=True
    )
    author = StringRelatedField()

    def to_representation(self, instance):
        key = 0
        # 0 because KEY might be == None (if no was provided at moment of creation)
        try:
            if self.context['request'].auth:
                key = self.context['request'].auth.get('key')
        except AttributeError:
            pass

        if not instance.active:
            logger.warning('Inactive instance has been invoked; short_code: %s' % instance.short_code)

        ret = super().to_representation(instance)
        fields_to_pop = ['author', 'key', 'creator_ip', 'time_created', 'view_data_code']
        if (instance.author != self.context['request'].user) and (instance.key != key):
            [ret.pop(field, '') for field in fields_to_pop]
        return ret

    def validate_full_url(self, url):
        """
            Check that URL is valid.
        """
        if DOMAIN_NAME in url:
            raise serializers.ValidationError('URL can\'t redirect to this same site')

        if len(url) > MAX_URL_LENGTH:
            raise serializers.ValidationError('URL is too long (%s symbols max)' % MAX_URL_LENGTH)
        return url

    def validate_short_code(self, short_code):
        if short_code:
            if ShortUrl.objects.filter(short_code=short_code.lower()).exists():
                raise serializers.ValidationError('This alias is already taken.')

            if MIN_SHORTCODE_LENGTH > len(short_code) or len(short_code) > MAX_SHORTCODE_LENGTH:
                raise serializers.ValidationError('Alias must have length from %s to %s symbols.' %
                                                  (MIN_SHORTCODE_LENGTH, MAX_SHORTCODE_LENGTH))

            for i in short_code.lower():
                if i not in string.ascii_lowercase + '0123456789-_':
                    raise serializers.ValidationError('Only letters, numbers, and underscores in alias')

        return short_code

    def create(self, validated_data):
        obj = ShortUrl.objects.filter(full_url=self.validated_data['full_url'], do_collect_meta=False,
                                      alias=False, active=True)

        # if object already exists, we don't need to create it again.
        if not self.validated_data.get('do_collect_meta') and \
                len(obj) == 1 and not self.validated_data.get('short_code'):
            obj = obj[0]

            obj.creator_ip = self.context['request'].META['REMOTE_ADDR']
            if not self.context['request'].user.is_anonymous:
                obj.author = self.context['request'].user
            else:
                obj.author = None
            obj.time_created = datetime.datetime.now()

            return obj

        data = dict(validated_data).copy()

        data['active'] = True
        data['creator_ip'] = self.context['request'].META['REMOTE_ADDR']
        data['do_collect_meta'] = (lambda: True if validated_data.get('do_collect_meta') else False)()
        data['alias'] = (lambda: True if validated_data.get('short_code') else False)()

        if not validated_data.get('short_code'):
            data['short_code'] = get_shorturl(ShortUrl, SHORTCODE_BASE_LENGTH, check_for_existing_var='short_code')

        if data['do_collect_meta']:
            data['view_data_code'] = get_shorturl(ShortUrl, MAX_SHORTCODE_LENGTH + 1,
                                                  check_for_existing_var='view_data_code')
        if not self.context['request'].user.is_anonymous:
            data['author'] = self.context['request'].user
        else:
            try:
                if self.context['request'].auth is not None:
                    data['key'] = self.context['request'].auth['key']
            except AttributeError:
                pass

        return ShortUrl.objects.create(**data)

    class Meta:
        model = ShortUrl
        read_only_fields = ['alias', 'time_created', 'author', 'active', 'key', 'creator_ip', 'view_data_code']
        fields = ['short_code', 'full_url', 'do_collect_meta'] + read_only_fields


class VisitSerializer(serializers.ModelSerializer):
    permission_classes = [IsVisitOwner]

    shorturl = SlugRelatedField(
        slug_field='short_code',
        required=True,
        queryset=ShortUrl.objects.all()
    )
    time = DateTimeField(
        format='%d.%m.%Y %H:%M:%S',
        read_only=True
    )

    class Meta:
        model = Visit
        fields = '__all__'
