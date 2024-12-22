from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('direction',)}),
)

admin.site.register(Student, UserAdmin)
