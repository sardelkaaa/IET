from django.db import models


class Profession(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    knowledge = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'professions'
        verbose_name = 'Profession'
        verbose_name_plural = 'Professions'
        ordering = ('id',)

    def __str__(self):
        return self.name
