from django.db import models
from directions.models import Direction


class Discipline(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'disciplines'
        verbose_name = 'Discipline'
        verbose_name_plural = 'Disciplines'
        ordering = ('id',)

    def __str__(self):
        return self.name


class DisciplinesDirections(models.Model):
    id = models.BigAutoField(primary_key=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, blank=True, null=True)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, blank=True, null=True)
    semester = models.BigIntegerField()

    class Meta:
        db_table = 'disciplines-directions'
