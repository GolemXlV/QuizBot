from telegram.ext import BaseFilter


class FilterGetQuestion(BaseFilter):
    def filter(self, message):
        return message.text and 'пройти тест' in message.text.lower()


class FilterHelpCommand(BaseFilter):
    def filter(self, message):
        return message.text and 'помощь' in message.text.lower()


filter_get_question = FilterGetQuestion()
filter_help_command = FilterHelpCommand()
