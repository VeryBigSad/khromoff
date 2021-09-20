import json
import logging

logger = logging.getLogger(__name__)


def telegram_bot_view(request):
    logger.debug("New telegram event")
    process_telegram_event(json.loads(request.body))


def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)
