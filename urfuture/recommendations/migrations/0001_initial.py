# Generated by Django 5.1.4 on 2024-12-24 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionCompetencyCourseLinks',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('weight', models.IntegerField()),
            ],
            options={
                'db_table': 'profession_competency_course_links',
                'managed': False,
            },
        ),
    ]
