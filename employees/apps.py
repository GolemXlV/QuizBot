from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    name = 'employees'
    verbose_name = _("Employee management")
