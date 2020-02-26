import time

from polls.utils import send_report
from .models import Question
from employees.models import Employee
from quizbot.celery_app import app as celery_app
from celery import group
from constance import config
from datetime import timedelta
from django.utils import timezone


@celery_app.task
def start_poll(delta_period=5):
    from quizbot import settings
    from tgbot.base import TelegramBotApi

    api = TelegramBotApi(token=settings.DEFAULT_BOT_TOKEN)

    now = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
    day = now.weekday() + 1

    start_time = now - timedelta(minutes=delta_period)
    end_time = now - timedelta(seconds=1)

    job = group([send_poll.s(api, employee.id, employee.tguser.tg_id, employee.department_id) for employee
                 in Employee.objects.filter(tguser__isnull=False, department__isnull=False,
                                            department__days_for_poll__contains=[day],
                                            department__time_for_poll__range=[start_time.time(), end_time.time()])])
    res = job.apply_async()


@celery_app.task
def send_poll(api, emp_id, tg_id, dept_id):
    from tgbot.handlers import send_question

    poll = api.create_poll(emp_id, config.POLL_QUESTIONS_NUM, dept_id)
    api.bot.send_message(tg_id, config.DEFAULT_START_POLL_MSG)
    question_id = api.get_next_question_id(poll)
    return send_question(api, question_id, tg_id, poll.pk, poll.state)
    # return get_question_handler(api, uid=tg_id, qid=question_id, pid=poll.pk, st=poll.state)


@celery_app.task
def send_email(period, ):
    send_report(period)


@celery_app.task
def do_some_queries():
    time.sleep(10)
    return Question.objects.count()


@celery_app.task
def query_every_five_mins():
    pass
