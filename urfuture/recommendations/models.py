from django.db import models
from professions.models import Profession
from disciplines.models import Discipline
from courses.models import Competency, Course


class ProfessionCompetencyCourseLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True)
    competency = models.ForeignKey(Competency, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.IntegerField()
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'profession_competency_course_links'

    def __str__(self):
        return f'Дисциплина: {self.discipline} Курс: {self.discipline} Профессия: {self.profession} Вес: {self.weight}'
