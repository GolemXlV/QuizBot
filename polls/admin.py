from django.contrib import admin
from .models import Question, Choice, Poll

# Register your models here.
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
