from django import template
from django.template.defaultfilters import stringfilter
import pymorphy2

register = template.Library()
morph = pymorphy2.MorphAnalyzer()


@register.filter
@stringfilter
def smart_plural(value, number):
    words = str(value).split()
    for i in range(len(words)):
        word = morph.parse(words[i])[0]
        word = word.make_agree_with_number(number).word
        words[i] = word if i > 1 else word.capitalize()

    return " ".join(words)
