from django.contrib.auth.models import AbstractUser
from django.db import models
from directions.models import Directions


class Student(AbstractUser):
    direction = models.ForeignKey(
        Directions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Направление'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
