from django import forms
from django.forms import MultipleChoiceField

from .models import Employee


class EmployeeForm(forms.ModelForm):
    days_for_poll = MultipleChoiceField(choices=Employee.days_of_week)

    class Meta:
        model = Employee
        exclude = []
