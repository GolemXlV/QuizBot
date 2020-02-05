from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = _("Poll")
