from django.db import models
from django.contrib.postgres.fields import ArrayField
from disciplines.models import Discipline
from directions.models import Direction


class Course(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    knowledge = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING, null=True, blank=True)
    tags = models.TextField(blank=True, null=True)
    directions = ArrayField(
        base_field=models.IntegerField(),
        blank=True,
        null=True,
        db_column='direction_id',
        help_text='Список ID направлений'
    )

    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Competency(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    tags = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'competencies'
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'
        ordering = ('id',)

    def __str__(self):
        return self.name
