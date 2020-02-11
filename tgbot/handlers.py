from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, Filters, run_async, CallbackQueryHandler
import json
from collections import OrderedDict

# from employees.models import Message
from .base import TelegramBotApi
from .utils import logger, build_menu, encode_callback_data, decode_callback_data
import random
from .filters import FilterGetQuestion, FilterHelpCommand
#
# button_list =[
#     InlineKeyboardButton()
# ]


@run_async
def start_handler(api: TelegramBotApi, update):
    logger.info('START: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    # Message.from_update(api, update)
    user = api.get_user(update.message.chat_id)
    if not user:
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Предоставить номер", request_contact=True)]],
                                           resize_keyboard=True, one_time_keyboard=True)
        api.bot.send_message(update.message.chat_id, "Запрос номера мобильного телефона", reply_markup=reply_markup)
    else:
        buttons_list = [
            KeyboardButton("Пройти тест"),
            KeyboardButton("Помощь"),
        ]
        reply_markup = ReplyKeyboardMarkup(build_menu(buttons_list, n_cols=len(buttons_list)), resize_keyboard=True)
        msg = """Выберите пункт меню. Для прохождения случайного теста используйте команды: 
        /get_question для получения случайного вопроса
        /start_poll для того чтобы начать тест 
        /help для помощи."""
        api.bot.send_message(update.message.chat_id, msg, reply_markup=reply_markup)


@run_async
def contact_callback(api: TelegramBotApi, update):
    logger.info('CONTACT_CALLBACK: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    user = api.get_user(update.message.chat_id)
    if user:
        msg = f"Вы уже авторизованы как пользователь {user.employee.full_name} " \
              f"из департамента {user.employee.department}"
        api.bot.send_message(update.message.chat_id, msg)
        return
    contact = update.effective_message.contact
    phone = contact.phone_number
    employee = api.get_employee_by_phone(phone)
    if not employee:
        msg = "Вас нет в базе, обратитесь в офис по таким-то контактам."
    else:
        api.create_user(update.message.chat_id, employee)
        msg = f"Вы успешно авторизованы как пользователь {employee.full_name} из департамента {employee.department}."
    api.bot.send_message(update.message.chat_id, msg)


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
        api.bot.send_message(callback_obj['u'], f"Комментарий: {answer.comment}. Получено баллов: {answer.votes}")
        if "pid" in callback_obj and "st" in callback_obj:
            callback_obj["st"] = int(callback_obj["st"]) + 1
            poll = api.update_poll(callback_obj["pid"], callback_obj["st"], answer.votes)
            if not poll.closed:
                question_id = api.get_next_question_id(poll)
                get_question_handler(api, update, uid=callback_obj["u"], qid=question_id, pid=poll.pk, st=int(poll.state))
            else:
                api.bot.send_message(callback_obj['u'], f"Тест завершён. Набрано баллов: {poll.votes}")

    else:
        api.bot.send_message(callback_obj['u'], "Неправильный запрос")


@run_async
def get_question_handler(api: TelegramBotApi, update, uid=None, qid=None, pid=None, st=None):
    uid = update.message.chat_id if update.message else uid
    # logger.info('GET_QUESTION: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    if qid is not None:
        question = api.get_question(qid)
    else:
        question = api.get_random_question()
    choice_data = [(dict(c="a", u=uid, cid=choice.id, qid=qid, pid=pid, st=st),
                    choice.choice_text) for choice in question.choice_set.all()]
    print([encode_callback_data(data) for data, ch_text in choice_data])
    buttons_list = [InlineKeyboardButton(ch_text, callback_data=encode_callback_data(data))
                                   for data, ch_text in choice_data]
    random.shuffle(buttons_list)  # reorder items
    reply_markup = InlineKeyboardMarkup(build_menu(buttons_list, n_cols=1), )
    api.bot.send_message(uid, f"Вопрос{' №' + str(st+1) if st is not None else ''}: {question.question_text}",
                         reply_markup=reply_markup)


@run_async
def help_handler(api: TelegramBotApi, update):
    logger.info('HELP: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    api.bot.send_message(update.message.chat_id, "Это раздел помощи.")


@run_async
def start_poll_handler(api: TelegramBotApi, update):
    logger.info('START_POLL: Got message {} from {}'.format(update.message.text, update.message.chat_id))
    user = api.get_user(update.message.chat_id)
    if not user:
        api.bot.send_message(update.message.chat_id, "Вы не авторизовались.")
        return
    poll = api.create_poll(user.employee_id)
    api.bot.send_message(update.message.chat_id, f"Тест №{poll.id} начался...")
    question_id = api.get_next_question_id(poll)
    return get_question_handler(api, update, qid=question_id, pid=poll.pk, st=poll.state)


handlers = [
    CommandHandler("start", start_handler),
    CommandHandler("get_question", get_question_handler),
    CommandHandler("start_poll", start_poll_handler),
    CommandHandler("help", help_handler),
    # MessageHandler(FilterGetQuestion, get_question_handler),
    # MessageHandler(FilterHelpCommand, help_handler),
    CallbackQueryHandler(answer_handler),
]
