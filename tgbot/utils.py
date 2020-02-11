import logging, json
from collections import OrderedDict

logger = logging.getLogger('bot')


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def encode_callback_data(data: dict, sep1=',', sep2=":"):
    return sep1.join(map(lambda x: "%s%s%s" % (x[0], sep2, x[1]) if x[1] is not None else "", data.items()))


def decode_callback_data(encoded_obj: str, sep1=",", sep2=":"):
    encoded_obj = encoded_obj.split(sep1)
    encoded_obj = map(lambda x: x.split(sep2), encoded_obj)
    encoded_obj = filter(lambda x: len(x) > 1, encoded_obj)
    encoded_obj = list(encoded_obj)
    return dict(encoded_obj)
