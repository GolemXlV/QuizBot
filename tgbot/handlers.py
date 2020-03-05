from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import re
from collections import OrderedDict

# from employees.models import Message
from .base import TelegramBotApi
from .utils import logger, build_menu, encode_callback_data, decode_callback_data, lookahead
import random
from .filters import FilterGetQuestion, FilterHelpCommand, filter_get_question, filter_help_command
from constance import config

#
# button_list =[
#     InlineKeyboardButton()
# ]


def send_question(api, qid, uid, pid, st):

    if qid is not None:
        question = api.get_question(qid)
    else:
        question = api.get_random_question()
    choices = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
    random.shuffle(choices)
    choice_data = [(dict(c="a", u=uid, cid=choice[0], qid=qid, pid=pid, st=st), f"Вариант {i}")
                   for i, choice in enumerate(choices, 1)]
    logger.info([encode_callback_data(data) for data, ch_text in choice_data])
    buttons_list = [InlineKeyboardButton(ch_text, callback_data=encode_callback_data(data))
                                   for data, ch_text in choice_data]
    # random.shuffle(buttons_list)  # reorder items
    reply_markup = InlineKeyboardMarkup(build_menu(buttons_list, n_cols=2), )
    api.bot.send_message(uid, f"ВОПРОС {st+1}/{config.POLL_QUESTIONS_NUM}:  {question.question_text}")

    for (i, choice), has_more in lookahead(enumerate(choices, 1)):
        if has_more:
            api.bot.send_message(uid, f"ВАРИАНТ {i}:  {choice[1]}")
        else:
            api.bot.send_message(uid, f"ВАРИАНТ {i}:  {choice[1]}", reply_markup=reply_markup)


def send_buttons(api: TelegramBotApi, update):
    buttons_list = [
        KeyboardButton("Пройти тест"),
    #     KeyboardButton("Помощь"),
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(buttons_list, n_cols=len(buttons_list)), resize_keyboard=True)
    msg = config.DEFAULT_AFTER_AUTH_MSG
    api.bot.send_message(update.message.chat_id, msg,
                         reply_markup=reply_markup
                         )


@run_async
def start_handler(api: TelegramBotApi, update):
    logger.info('START: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    # Message.from_update(api, update)
    user = api.get_user(update.message.chat_id)
    if not user:
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Предоставить номер", request_contact=True)]],
                                           resize_keyboard=True, one_time_keyboard=True)
        api.bot.send_message(update.message.chat_id, config.DEFAULT_ASK_NUMBER_MSG, reply_markup=reply_markup)
    else:
        send_buttons(api, update)


@run_async
def contact_callback(api: TelegramBotApi, update):
    logger.info('CONTACT_CALLBACK: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    user = api.get_user(update.message.chat_id)
    if user:
        msg_data = dict(name=user.employee.full_name, department=user.employee.department)
        msg = config.DEFAULT_SUCCESS_AUTH_MSG % msg_data
        api.bot.send_message(update.message.chat_id, msg)
        return
    contact = update.effective_message.contact
    phone = "".join(re.findall("\d", str(contact.phone_number)))
    employee = api.get_employee_by_phone(phone)
    if not employee:
        msg = config.DEFAULT_PHONE_NUMBER_ERROR_MSG
        api.bot.send_message(update.message.chat_id, msg)
    else:
        api.create_user(update.message.chat_id, employee)
        msg_data = dict(name=employee.full_name, department=employee.department)
        msg = config.DEFAULT_SUCCESS_AUTH_MSG % msg_data
        api.bot.send_message(update.message.chat_id, msg)
        send_buttons(api, update)


@run_async
def answer_handler(api: TelegramBotApi, update):
    callback_data = update.callback_query.data
    print(f"callback_data: {callback_data}")
    callback_obj = decode_callback_data(callback_data)
    print(f"callback_obj: {callback_obj}")
    if callback_obj["c"] != "a":
        api.bot.send_message(update.message.chat_id, "Неизвестная команда...")
        return
    answer = api.get_answer(callback_obj['cid'])
    if answer:
        if "pid" in callback_obj and "st" in callback_obj:
            poll = api.get_poll(callback_obj["pid"])
            if int(callback_obj["st"]) < poll.state:
                api.bot.send_message(callback_obj['u'], f"Вы уже ответили на этот вопрос.")
                return
            if poll.closed:
                api.bot.send_message(callback_obj['u'], f"Вы уже прошли этот тест.")
                return

            msg_data = dict(comment=answer.comment, votes=answer.votes)
            msg = config.DEFAULT_ANSWER_MSG % msg_data
            api.bot.send_message(callback_obj['u'], msg)
            callback_obj["st"] = int(callback_obj["st"]) + 1
            poll = api.update_poll(callback_obj["pid"], callback_obj["st"], answer.votes)
            if not poll.closed:
                question_id = api.get_next_question_id(poll, callback_obj["st"])
                get_question_handler(api, update, uid=callback_obj["u"], qid=question_id, pid=poll.pk, st=int(poll.state))
            else:
                msg_data = dict(votes=poll.votes, max_votes=poll.max_votes)
                msg = config.DEFAULT_POLL_END_MSG % msg_data
                api.bot.send_message(callback_obj['u'], msg)
        else:
            msg_data = dict(comment=answer.comment, votes=answer.votes)
            msg = config.DEFAULT_ANSWER_MSG % msg_data
            api.bot.send_message(callback_obj['u'], msg)

    else:
        api.bot.send_message(callback_obj['u'], "Неправильный запрос")


@run_async
def get_question_handler(api: TelegramBotApi, update=None, uid=None, qid=None, pid=None, st=None):
    uid = update.message.chat_id if update and update.message else uid
    # logger.info('GET_QUESTION: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    send_question(api, qid, uid, pid, st)


@run_async
def help_handler(api: TelegramBotApi, update):
    logger.info('HELP: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    api.bot.send_message(update.message.chat_id, config.DEFAULT_AFTER_AUTH_MSG)


@run_async
def start_poll_handler(api: TelegramBotApi, update):
    logger.info('START_POLL: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    user = api.get_user(update.message.chat_id)
    if not user:
        api.bot.send_message(update.message.chat_id, "Вы не авторизовались.")
        return
    poll = api.create_poll(user.employee_id, config.POLL_QUESTIONS_NUM, user.employee.department_id)
    api.bot.send_message(update.message.chat_id, config.DEFAULT_START_POLL_MSG)
    question_id = api.get_next_question_id(poll)
    return get_question_handler(api, update, uid=user.tg_id, qid=question_id, pid=poll.pk, st=poll.state)


handlers = [
    CommandHandler("start", start_handler),
    # CommandHandler("get_question", get_question_handler),
    CommandHandler("start_poll", start_poll_handler),
    CommandHandler("help", help_handler),
    MessageHandler(filter_get_question, start_poll_handler),
    # MessageHandler(filter_help_command, help_handler),
    MessageHandler(Filters.contact, contact_callback),
    CallbackQueryHandler(answer_handler),
]
