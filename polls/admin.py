from django.contrib import admin
from .models import Question, Choice, Poll


class PollAdmin(admin.ModelAdmin):
    list_display = ("employee", "state", "closed", "votes", "date_created", "date_modified", "date_closed")
    list_filter = ("state", "closed", "date_created", "date_modified", "date_closed")
    search_fields = ['employee', "votes"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date")
    list_filter = ("pub_date",)
    search_fields = ['question_text']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "comment", "votes")
    list_filter = ("votes",)
    search_fields = ['choice_text', "comment"]


# Register your models here.
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
