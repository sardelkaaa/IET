from django.contrib.auth.models import AbstractUser
from django.db import models
from directions.models import Direction
from professions.models import Profession


class Student(AbstractUser):
    username = None
    email = models.EmailField(
        'Email',
        unique=True,
        blank=False,
        null=False
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=150,
        blank=False,
        null=False
    )
    direction = models.ForeignKey(
        Direction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Направление'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.patronymic or ""} {self.last_name}'.strip()
