from django.contrib import admin
from .models import Courses, Competencies

admin.site.register((Courses, Competencies))
