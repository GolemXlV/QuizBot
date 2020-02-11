from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from .messages import PHONE_VALIDATION_MSG

# Create your models here.


class Employee(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=PHONE_VALIDATION_MSG)
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    blank=False, verbose_name=_("Phone number"))
    full_name = models.CharField(max_length=300, verbose_name=_("Full name"))
    department = models.CharField(max_length=100, verbose_name=_("Department"))

    def __str__(self):
        return f"Сотрудник №{self.pk}"

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class TGUser(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)

    tg_id = models.CharField(max_length=300, verbose_name=_("Telegram ID"))
    username = models.CharField(max_length=300, verbose_name=_("Telegram user name"))
    first_name = models.CharField(max_length=300, verbose_name=_("Telegram first name"))
    last_name = models.CharField(max_length=300, verbose_name=_("Telegram last name"))

    def __str__(self):
        return f"Телеграм ID №{self.pk}"

    class Meta:
        verbose_name = _("Telegram user")
        verbose_name_plural = _("Telegram users")
