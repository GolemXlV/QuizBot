import os
from .settings import *

ALLOWED_HOSTS = ['app']
DEBUG = False
PRODUCTION = True


def env(name, default=None, type=None):
    value = os.environ.get(name, default)
    return type(value) if type is not None else value


DEFAULT_BOT_TOKEN = env('BOT_TOKEN', None)

TG_WEBHOOK = os.environ.get('BOT_WEBHOOK') == 'true'
TG_WEBHOOK_PORT = int(os.environ.get('BOT_WEBHOOK_PORT', 5555))


EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')