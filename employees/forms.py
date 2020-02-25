from django import forms
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _

from .models import DailyTaskModel, Employee, Department


class DailyTaskMixin(forms.Form):
    days_for_poll = MultipleChoiceField(choices=DailyTaskModel.days_of_week, label=_("Days for poll"), localize=True)


class DepartmentForm(DailyTaskMixin, forms.ModelForm):

    class Meta:
        model = Department
        exclude = []


class EmployeeForm(DailyTaskMixin, forms.ModelForm):

    class Meta:
        model = Employee
        exclude = []
