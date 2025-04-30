from django.db import models


class Direction(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'directions'
        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'
        ordering = ('id',)

    def __str__(self):
        return self.name
