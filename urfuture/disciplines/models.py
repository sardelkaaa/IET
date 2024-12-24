from django.db import models
from directions.models import Directions


class Disciplines(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disciplines'
        verbose_name = 'Discipline'
        verbose_name_plural = 'Disciplines'
        ordering = ('id',)

    def __str__(self):
        return self.name


class DisciplinesDirections(models.Model):
    id = models.BigAutoField(primary_key=True)
    discipline = models.ForeignKey(Disciplines, models.DO_NOTHING)
    direction = models.ForeignKey(Directions, models.DO_NOTHING, blank=True, null=True)
    semester = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'disciplines-directions'
