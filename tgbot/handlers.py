from telegram.ext import MessageHandler, Filters, run_async

# from employees.models import Message
from .base import TelegramBotApi
from .utils import logger


@run_async
def echo_handler(api: TelegramBotApi, update):
    logger.info('Got message {} from {}'.format(update.message.text, update.message.chat_id))
    # Message.from_update(api, update)
    api.bot.send_message(update.message.chat_id, update.message.text)


handlers = [
    MessageHandler(Filters.text, echo_handler)
]
