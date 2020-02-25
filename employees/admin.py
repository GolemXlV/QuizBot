from django.contrib import admin

from employees.forms import EmployeeForm, DepartmentForm
from .models import Employee, TGUser, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ['name', ]
    form = DepartmentForm


class TGUserInline(admin.TabularInline):
    model = TGUser
    min_num = 1
    max_num = 1
    readonly_fields = ('tg_id', 'username', 'first_name', 'last_name')
    can_delete = False


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("department", "full_name", "phone_number", "tguser")
    list_filter = ['department',]
    search_fields = ["full_name", "department__name", "phone_number", "tguser"]
    form = EmployeeForm
    inlines = [TGUserInline]


# Register your models here.
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
