from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.db import models
from .managers import QuestionManager, PollManager
from employees.models import Employee
from datetime import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=500, verbose_name=_("Question text"))
    pub_date = models.DateTimeField(verbose_name=_('Date added'), auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return f"Вопрос: {self.question_text}"

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"))
    choice_text = models.CharField(max_length=200, verbose_name=_("Answer text"))
    comment = models.CharField(max_length=200, verbose_name=_("Comment"))
    votes = models.IntegerField(default=0, verbose_name=_("Vote"))

    def __str__(self):
        return f"Ответ: {self.choice_text}"

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")


class Poll(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"))
    questions = models.ManyToManyField(Question, verbose_name=_("Questions"))
    state = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("State num"))
    closed = models.BooleanField(default=False, verbose_name=_("Is closed?"))
    votes = models.IntegerField(default=0, verbose_name=_("Votes"))

    max_votes = models.IntegerField(default=0, verbose_name=_("Maximum Votes"))

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date created"))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_("Date updated"))
    date_closed = models.DateTimeField(blank=True, null=True, verbose_name=_("Date closed"))

    objects = PollManager()

    def __str__(self):
        return f"Голосование №{self.pk}"

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    def save(self, **kwargs):
        if self.state is None:
            self.state = 0
        if self.id and self.questions.count() > 0:
            self.max_votes = sum(map(lambda x: x.max_votes, self.questions.annotate(max_votes=Max('choice__votes'))))
        if self.id and self.state >= self.questions.count():
            self.closed = True
            self.date_closed = datetime.now()
        super().save(**kwargs)
