from django.conf import settings
import logging

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    """
    Detect the user's browser language settings and activate the language.
    If the default language is not supported, try secondary options.  If none of the
    user's languages are supported, then do nothing.
    """

    def is_supported_language(self, language_code):
        supported_languages = dict(settings.LANGUAGES).keys()
        return language_code in supported_languages

    def get_browser_language(self, request):
        browser_language_code = request.META.get('HTTP_ACCEPT_LANGUAGE', None)
        if browser_language_code is not None:
            logging.info('HTTP_ACCEPT_LANGUAGE: %s' % browser_language_code)
            languages = [language for language in browser_language_code.split(',') if
                         '=' not in language]
            for language in languages:
                language_code = language.split('-')[0]
                if self.is_supported_language(language_code):
                    return language_code
                else:
                    logging.info('Unsupported language found: %s' % language_code)

    def process_request(self, request):
        language_code = self.get_browser_language(request)
        if language_code:
            translation.activate(settings.LANGUAGE_CODE)
