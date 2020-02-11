from telegram.ext import BaseFilter


class FilterGetQuestion(BaseFilter):
    def filter(self, message):
        return 'пройти тест' in message.text.lower()


class FilterHelpCommand(BaseFilter):
    def filter(self, message):
        return 'помощь' in message.text.lower()
