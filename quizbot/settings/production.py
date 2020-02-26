import sys
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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
    }
}