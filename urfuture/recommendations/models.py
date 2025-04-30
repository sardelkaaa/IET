from django.db import models
from professions.models import Profession
from disciplines.models import Discipline
from courses.models import Competency, Course


class ProfessionCompetencyCourseLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    profession = models.ForeignKey(Profession, models.DO_NOTHING)
    competency = models.ForeignKey(Competency, models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    weight = models.IntegerField()
    discipline = models.ForeignKey(Discipline, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profession_competency_course_links'

    def __str__(self):
        return f'Дисциплина: {self.discipline} Курс: {self.discipline} Профессия: {self.profession} Вес: {self.weight}'
