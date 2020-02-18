from django.contrib import admin

from employees.forms import EmployeeForm
from .models import Employee, TGUser


class TGUserInline(admin.TabularInline):
    model = TGUser
    min_num = 1
    max_num = 1
    readonly_fields = ('tg_id', 'username', 'first_name', 'last_name')
    can_delete = False


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("department", "full_name", "phone_number", "tguser")
    search_fields = ['full_name', "department", "phone_number", "tguser"]
    form = EmployeeForm
    inlines = [TGUserInline]


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
