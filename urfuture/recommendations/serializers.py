from rest_framework import serializers


class BestCourseSerializer(serializers.Serializer):
    discipline = serializers.CharField()
    course = serializers.CharField()
    weight = serializers.FloatField(allow_null=True)
