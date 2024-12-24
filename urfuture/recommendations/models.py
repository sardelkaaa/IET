from django.db import models
from professions.models import Professions
from disciplines.models import Disciplines
from courses.models import Competencies, Courses


class ProfessionCompetencyCourseLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    profession = models.ForeignKey(Professions, models.DO_NOTHING)
    competency = models.ForeignKey(Competencies, models.DO_NOTHING)
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    weight = models.IntegerField()
    discipline = models.ForeignKey(Disciplines, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profession_competency_course_links'

    def __str__(self):
        return f'Дисциплина: {self.discipline} Курс: {self.discipline} Профессия: {self.profession} Вес: {self.weight}'
