import traceback
from abc import abstractmethod

import telegram
import telegram.utils.request
from cached_property import cached_property

# from employees.models import TGUser
from employees.models import TGUser, Employee
from polls.models import Question, Choice, Poll
import random


class TelegramBotApi:
    def __init__(self, token):
        self.token = token

    @cached_property
    def bot(self) -> telegram.Bot:
        bot = telegram.Bot(self.token)

        return bot

    @abstractmethod
    def start_bot(self, handlers):
        pass

    def get_user_data(self, user_id):
        chat = self.bot.get_chat(user_id)
        return chat.username or '', chat.first_name or '', chat.last_name or ''

    def update_user_data(self, user):
        try:
            username, name, last_name = self.get_user_data(user.tg_id)
            user.last_name = last_name
            user.first_name = name
            user.username = username
        except:
            print('Error getting user data')
            traceback.print_exc()
        user.save()

    def get_user(self, tg_id) -> TGUser:
        user = TGUser.objects.filter(tg_id=tg_id).first()
        return user

    def get_employee_by_phone(self, phone_number):
        print(phone_number)
        employee = Employee.objects.filter(phone_number=phone_number).first()
        return employee

    def create_user(self, tg_id, employee: Employee):
        user = TGUser(tg_id=tg_id, employee=employee)
        user.save()
        if user.last_name == '' and user.first_name == '' and user.username == '':
            self.update_user_data(user)
        return user

    def get_question(self, question_id=None) -> Question:
        if question_id is not None:
            return Question.objects.filter(pk=question_id).first()

    def get_random_question(self):
        question = Question.objects.get_questions()
        return random.choice(question)

    def get_answer(self, answer_id) -> Choice:
        answer = Choice.objects.filter(pk=answer_id).first()
        return answer

    def create_poll(self, employee_id, questions_num=3) -> Poll:
        q_ids = Question.objects.get_questions(num=questions_num, flat=True)
        poll = Poll.objects.create_poll(employee_id=employee_id, questions_ids=q_ids)
        return poll

    def get_poll(self, poll_id):
        return Poll.objects.filter(pk=poll_id).first()

    def get_next_question_id(self, poll):
        question_id = poll.questions.values_list('id', flat=True)[poll.state]
        return question_id

    def update_poll(self, poll_id, state, vote):
        poll = self.get_poll(poll_id)
        if poll:
            poll.state = state
            poll.votes += vote
            poll.save()
        return poll

