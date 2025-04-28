from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('direction',)}),
    )
