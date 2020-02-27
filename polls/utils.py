from collections import namedtuple, defaultdict
from datetime import datetime, timedelta, time

from constance import config
from django.core.mail import send_mail
from django.db import connection

ReportEntry = namedtuple('ReportEntry', 'days votes max_votes')
processed_data = defaultdict(lambda: ReportEntry(days=[], votes=[], max_votes=[]))
email_data = defaultdict(lambda: processed_data)


def send_report(period=7):
    start = datetime.combine(datetime.now().date(), time())
    end = datetime.combine(datetime.now().date() - timedelta(period), time())

    with connection.cursor() as cursor:
        cursor.execute("""select full_name, phone_number, e.day, votes, max_votes, email from (
        select e.id, full_name, phone_number, department_id, d.day, d.email from employees_employee e 
        inner join (select id, cast(unnest(days_for_poll) as integer) as day, email from employees_department) as d 
        on d.id=e.department_id) as e 
        left join(select employee_id, extract(dow from date_created) as day, max(votes) as votes, 
        max(max_votes) as max_votes from polls_poll where date_created between %s and %s group by 1, 2) p 
        on p.employee_id = e.id and p.day = e.day""", [end, start])
        rows = cursor.fetchall()
    for row in rows:
        full_name, phone_number, day, votes, max_votes, email = row
        processed_data[f"{phone_number}\t{full_name}"].days.append(day)
        processed_data[f"{phone_number}\t{full_name}"].votes.append(votes)
        processed_data[f"{phone_number}\t{full_name}"].max_votes.append(max_votes)
        email_data["%s" % ",".join(email)] = processed_data

    # headers = "Сотрудник|Номер телефона|Понедельник|Вторник|Среда|Четверг|Пятница|Суббота|Воскресенье".split('|')
    # stat_list = [",".join(headers)]
    for email, data in email_data.items():
        stat_list = []
        for user, entry in data.items():
            user_entry = []
            for i in range(period):
                try:
                    day = entry.days[i]
                except:
                    user_entry.append("---")
                else:
                    user_entry.append(f"{entry.votes[i]}/{entry.max_votes[i]}" if entry.votes[i] is not None else "XXX")
            stat_list.append(", ".join(user_entry) + f"\t{user}")
        msg = "\n".join(stat_list)
        msg += config.DEFAULT_EMAIL_PS_MSG
        send_mail(config.DEFAULT_SUBJECT_FOR_EMAIL_SENDING, msg, config.DEFAULT_FROM_EMAIL,
                  email.split(","))
