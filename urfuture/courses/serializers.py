from django.db.models import Min, Max
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    discipline = serializers.CharField(
        source='discipline.name', read_only=True)
    semester = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'discipline', 'semester')

    def get_semester(self, obj):
        if obj.min_sem is None:
            return None
        return (
            str(obj.min_sem)
            if obj.min_sem == obj.max_sem
            else f"{obj.min_sem}-{obj.max_sem}"
        )
