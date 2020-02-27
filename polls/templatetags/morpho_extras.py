from django import template
from django.template.defaultfilters import stringfilter
import pymorphy2

register = template.Library()
morph = pymorphy2.MorphAnalyzer()


@register.filter
@stringfilter
def smart_plural(value):
    words = str(value).split()
    word = morph.parse(words.pop())[0]
    word = word.inflect({'plur', 'gent'}).word
    words.append(word if len(words) > 0 else word.capitalize())

    return " ".join(words)
