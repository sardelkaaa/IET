from django.contrib import admin
from .models import Course, Competency

admin.site.register((Course, Competency))
