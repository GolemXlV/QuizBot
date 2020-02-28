from django import forms
from .models import Choice
from django.utils.translation import gettext_lazy as _


class ChoiceForm(forms.ModelForm):
    comment = forms.CharField(max_length=200, widget=forms.TextInput({'size': '92'}), label=_("Comment"))

    class Meta:
        model = Choice
        exclude = []

