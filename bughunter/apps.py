import logging

import requests
from django.apps import AppConfig
from django_log_to_telegram.log import AdminTelegramHandler, TelegramFormatter

from khromoff import settings

logger = logging.getLogger('khromoff.utils.telegram_logging')


class BughunterConfig(AppConfig):
    name = 'bughunter'


class TelegramLogFormatter(TelegramFormatter):
    def format(self, record):
        try:
            a = 'ERROR: http500 page:\n' + super().format(record) + '\n'
            request = record.request
            a += 'view_name: %s\n' % request.resolver_match.view_name
            a += 'POST data: %s\n' % dict(request.POST)
            a += 'GET data: %s' % dict(request.GET)
        except AttributeError:
            a = record.message

        return str(a)


class TelegramLogHandler(AdminTelegramHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff_ids = settings.STAFF_TELEGRAM_IDS

        self.setFormatter(TelegramLogFormatter())

    def emit(self, record):
        if not self.bot_data:
            from django_log_to_telegram.models import BotData
            self.bot_data, created = BotData.objects.get_or_create(
                bot_token=self.bot_token
            )
        self.notify_all_staff(self.format(record))

    def notify_all_staff(self, message):
        for i in self.staff_ids:
            self.send_message(message, i)

    def send_message(self, message, tg_id=None):
        if tg_id is None:
            tg_id = self.bot_data.chat_id
        message_url = '{bot_url}sendMessage'.format(
            bot_url=self.bot_data.bot_url()
        )
        r = requests.post(message_url, json={
            "chat_id": self.bot_data.chat_id,
            "text": message,
            "parse_mode": 'HTML',
        })
        if r.status_code != 200:
            logger.critical('Message wasn\'t sent. Response data: %s' % r.json())

        return r
