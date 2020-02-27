"""
Django settings for quizbot project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'knqf_df05m-w9o^ct=9srrr@i9!50xt05w&011e8%-3x-hj38j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance',
    'constance.backends.database',
    'polls.apps.PollsConfig',
    'employees.apps.EmployeesConfig',
    'django_celery_beat',
    'django_celery_results',
]

CONSTANCE_CONFIG = {
    'POLL_QUESTIONS_NUM': (3, _("Number of questions per poll.")),
    'DEFAULT_ASK_NUMBER_MSG': ("""Здравствуйте! 
    Нам необходимо проверить Ваш телефон по базе данных. 
    Пожалуйста, нажмите кнопку «Запрос номера мобильного телефона» внизу экрана""", _("Default message for request contact")),
    'DEFAULT_SUCCESS_AUTH_MSG': (f"Вы успешно авторизованы как пользователь «%(name)s» из подразделения «%(department)s»",
                                     _("Default message for user after successful authorization")),
    'DEFAULT_START_POLL_MSG': (f"Здравствуйте! Начнём сегодняшнее тестирование", _("Default message for start poll")),
    'DEFAULT_AFTER_AUTH_MSG': ("""Итак, начиная с настоящего момента, чат-бот «Сержант» регулярно (в дни недели, указанные руководителем) 
    будет задавать вопросы по Вашей технологической или должностной инструкции. Для ответа нажимайте соответствующую кнопку внизу экрана Telegram. 
    Баллы за правильные ответы (отдельно за каждый день) суммируются. Итоговый отчёт в конце недели придёт на емаил руководителю. 
    Для повторного получения данной информации передайте боту команду /help 
    Тестирование прекратится, когда руководитель заблокирует ваш аккаунт в панели администратора""", _("Default message for bot after user complete authorization")),
    'DEFAULT_ANSWER_MSG': ("%(comment)s Начислено баллов за данный вопрос: %(votes)s", _("Message on answer the question")),
    'DEFAULT_POLL_END_MSG': ("""Поздравляю! Вы завершили тест на сегодня и набрали баллов: %(votes)s из %(max_votes)s максимально возможных.
    Хорошего дня!""", _("Message on poll ending")),
    'DEFAULT_PHONE_NUMBER_ERROR_MSG': ("Вас нет в базе, обратитесь в офис по таким-то контактам.", _("Message on incorrect authorization")),
    'DEFAULT_SUBJECT_FOR_EMAIL_SENDING': ("Тесты за неделю", _("Default subject for email sending")),
    'DEFAULT_FROM_EMAIL': ("bot@288077-yurdoos.tmweb.ru", _("Default from email for sending.")),
    'DEFAULT_TO_EMAIL': ("medvedev@zvezda-sb.ru", _("Default recipient email for sending (comma separator).")),
    'DEFAULT_EMAIL_PS_MSG': ("""

Расшифровка:
    I.	    3/8 	= 	3 правильных ответа на 8 вопросов
    II.	    --- 	= 	тест не назначался
    III.    ХХХ	=	пользователь не отвечал на вопросы теста
""", _("Default email post scriptum message.")),
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG_FIELDSETS = {
    'Настройки тестов': ('POLL_QUESTIONS_NUM', ),
    'Настройки бота': ('DEFAULT_ASK_NUMBER_MSG', 'DEFAULT_SUCCESS_AUTH_MSG', 'DEFAULT_START_POLL_MSG',
                       'DEFAULT_AFTER_AUTH_MSG', 'DEFAULT_ANSWER_MSG', 'DEFAULT_POLL_END_MSG',
                       'DEFAULT_PHONE_NUMBER_ERROR_MSG',),
    "Настройки рассылки": ('DEFAULT_SUBJECT_FOR_EMAIL_SENDING', 'DEFAULT_FROM_EMAIL', 'DEFAULT_TO_EMAIL',
                           'DEFAULT_EMAIL_PS_MSG'),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'quizbot.middleware.LanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quizbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quizbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = [
  ('ru', _('Russian')),
  ('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '../locale'),
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")

# Celery config
CELERY_BROKER_URL= 'pyamqp://rabbitmq:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_BEAT_SCHEDULE = {
    'queue_every_five_mins': {
        'task': 'polls.tasks.query_every_five_mins',
        'schedule': crontab(minute=5),
    },
}
