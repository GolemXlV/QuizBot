from django.contrib import admin
from .models import Question, Choice, Poll


class PollAdmin(admin.ModelAdmin):
    list_display = ("employee", "state", "closed", "votes", "date_created", "date_modified", "date_closed")
    list_filter = ("state", "closed", "date_created", "date_modified", "date_closed")
    search_fields = ['employee', "votes"]


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("department", "question_text", "pub_date")
    list_filter = ("department", "pub_date",)
    search_fields = ['question_text', 'choice__choice_text', "department"]
    inlines = [ChoiceInline]


# Register your models here.
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
