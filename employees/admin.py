from django.contrib import admin

from employees.forms import EmployeeForm
from .models import Employee, TGUser


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("department", "full_name", "phone_number", "tguser")
    search_fields = ['full_name', "department", "phone_number", "tguser"]
    form = EmployeeForm


class TGUserAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "employee", "username", "first_name", "last_name")
    search_fields = ["tg_id", 'username', "employee", "first_name", "last_name"]


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TGUser, TGUserAdmin)
