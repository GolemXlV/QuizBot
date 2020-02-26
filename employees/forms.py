from django import forms
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _

from .models import DailyTaskModel, Employee, Department


class DailyTaskMixin(forms.Form):
    days_for_poll = MultipleChoiceField(choices=DailyTaskModel.days_of_week, initial=DailyTaskModel.DEFAULT_CHOICE,
                                        label=_("Days for poll"), localize=True)


class DepartmentForm(DailyTaskMixin, forms.ModelForm):
    field_order = ['name', 'email', 'days_for_poll', 'time_for_poll']

    def order_fields(self, field_order):
        super().order_fields(field_order)
        # raise Exception(f"{field_order}: {self.fields.keys()}")

    class Meta:
        model = Department
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['name', 'email']:
                self.fields[field].widget = forms.TextInput(attrs={'size': '100'})


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = []
