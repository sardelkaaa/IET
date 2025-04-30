from rest_framework import serializers
from .models import Course
from disciplines.serializers import DisciplineSerializer


class CourseSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'discipline',
        )
