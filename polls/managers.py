from django.db.models import Manager, Max
import random


class QuestionManager(Manager):

    def get_questions(self, question_id=None, num=3, dept_id=None, flat=False):
        """Select random questions
        :returns List<Question>"""
        if question_id is not None:
            return self.filter(pk=question_id, department_id=dept_id).first()

        ids = list(self.filter(department_id=dept_id).values_list('id', flat=True))
        rand_ids = random.sample(ids, num if len(ids) > num else len(ids))

        if flat:
            return rand_ids
        return self.filter(pk__in=rand_ids)


class PollManager(Manager):

    def create_poll(self, employee_id, questions_ids):
        poll = self.create(employee_id=employee_id)
        poll.questions.add(*questions_ids)
        return poll
