import time

from quizbot.celery_app import app as celery_app
from quizbot import settings
from tgbot.base import TelegramBotApi
import datetime

bot = TelegramBotApi(token=settings.DEFAULT_BOT_TOKEN).bot


@celery_app.task
def start_poll():
    bot.sendMessage(chat_id=402671740, text='Working/{}'.format(datetime.datetime.now()))
