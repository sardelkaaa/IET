from django.db import models
from professions.models import Professions
from disciplines.models import Disciplines
from directions.models import Directions


class Courses(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    knowledge = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    discipline_id = models.ForeignKey(Disciplines, models.DO_NOTHING)
    tags = models.TextField(blank=True, null=True)
    direction_id = models.ForeignKey(Directions, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Competencies(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tags = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competencies'
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'
        ordering = ('id',)

    def __str__(self):
        return self.name


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
