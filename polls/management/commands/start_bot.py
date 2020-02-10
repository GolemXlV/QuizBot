import logging
import sys

from django.core.management.base import BaseCommand

from tgbot.handlers import handlers
from tgbot.sync_api import SyncBotApi
from tgbot.utils import logger
from quizbot import settings


class Command(BaseCommand):
    help = 'Run Bot'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--token', default=None)
        parser.add_argument('-d', '--debug', action='store_true')

    def handle(self, *args, **options):
        if options['debug']:
            tglogger = logging.getLogger("telegram")
            tglogger.setLevel(level=logging.DEBUG)
            tglogger.addHandler(logging.StreamHandler(sys.stdout))
        if options['token'] is None:
            token = settings.DEFAULT_BOT_TOKEN
        else:
            token = options['token']
        logger.info('Using token {}'.format(token))
        SyncBotApi(token).start_bot(handlers)
