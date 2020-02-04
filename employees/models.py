from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.db import models

# Create your models here.


class Employee(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    full_name = models.CharField(max_length=300)
    department = models.CharField(max_length=100)
