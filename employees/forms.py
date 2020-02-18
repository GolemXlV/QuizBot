from django import forms
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _

from .models import Employee


class EmployeeForm(forms.ModelForm):
    days_for_poll = MultipleChoiceField(choices=Employee.days_of_week, label=_("Days for poll"), localize=True)

    class Meta:
        model = Employee
        exclude = []
