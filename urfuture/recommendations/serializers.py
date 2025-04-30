from rest_framework import serializers
from courses.serializers import CourseSerializer


class BestCourseSerializer(serializers.Serializer):
    discipline = serializers.CharField()
    course = serializers.CharField()
    weight = serializers.FloatField(allow_null=True)
