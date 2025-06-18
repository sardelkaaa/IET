from disciplines.models import DisciplinesDirections
from rest_framework import serializers


class DisciplineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='discipline.id')
    name = serializers.CharField(source='discipline.name')
    semester = serializers.IntegerField()
    category = serializers.CharField(source='discipline.category')

    class Meta:
        model = DisciplinesDirections
        fields = ('id', 'name', 'semester', 'category')
