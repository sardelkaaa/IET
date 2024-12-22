from django.contrib import admin
from .models import Professions, Competencies, Courses, Disciplines, Directions

admin.site.register((Professions, Competencies,
                     Courses, Disciplines, Directions))
