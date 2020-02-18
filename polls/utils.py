from collections import namedtuple, defaultdict
from datetime import datetime, timedelta, time

from constance import config
from django.core.mail import send_mail
from django.db import connection

ReportEntry = namedtuple('ReportEntry', 'days votes max_votes')
processed_data = defaultdict(lambda: ReportEntry(days=[], votes=[], max_votes=[]))


def send_report(period=7):
    start = datetime.combine(datetime.now().date(), time())
    end = datetime.combine(datetime.now().date() - timedelta(period), time())

    with connection.cursor() as cursor:
        cursor.execute("""select full_name, phone_number, e.day, votes, max_votes from (
        select id, full_name, phone_number, cast(unnest(days_for_poll) as integer) as day from employees_employee) as e 
        left join(select employee_id, extract(dow from date_created) as day, max(votes) as votes, 
        max(max_votes) as max_votes from polls_poll where date_created between %s and %s group by 1, 2) p 
        on p.employee_id = e.id and p.day = e.day""", [end, start])
        rows = cursor.fetchall()
    for row in rows:
        full_name, phone_number, day, votes, max_votes = row
        processed_data[f"{full_name},{phone_number}"].days.append(day)
        processed_data[f"{full_name},{phone_number}"].votes.append(votes)
        processed_data[f"{full_name},{phone_number}"].max_votes.append(max_votes)

    headers = "Сотрудник|Номер телефона|Понедельник|Вторник|Среда|Четверг|Пятница|Суббота|Воскресенье".split('|')
    stat_list = [",".join(headers)]
    for user, entry in processed_data.items():
        user_entry = [f"{user}"]
        for i in range(period):
            try:
                day = entry.days[i]
            except:
                user_entry.append("-")
            else:
                user_entry.append(f"{entry.votes[i]}/{entry.max_votes[i]}" if entry.votes[i] is not None else "x")
        stat_list.append(",".join(user_entry))

    send_mail(config.DEFAULT_SUBJECT_FOR_EMAIL_SENDING, "\n".join(stat_list),
              config.DEFAULT_FROM_EMAIL, [config.DEFAULT_TO_EMAIL.split(",")])
