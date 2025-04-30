from disciplines.models import DisciplinesDirections
from rest_framework import serializers
from .models import Discipline


class DisciplineSerializer(serializers.ModelSerializer):
    semester = serializers.SerializerMethodField()

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'semester')

    def get_semester(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        direction = getattr(user, 'direction', None)
        if not direction:
            return None
        links = DisciplinesDirections.objects.filter(
            discipline=obj,
            direction=direction
        )
        if not links.exists():
            return None
        return links.first().semester
