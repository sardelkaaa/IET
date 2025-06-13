from rest_framework import serializers
from .models import Course
import re
import json


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


class CourseDetailSerializer(serializers.ModelSerializer):
    knowledge = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'description',
            'knowledge',
            'skills',
            'tags'
        )

    def _clean_numbered_lines(self, text):
        items = []
        for raw in text.splitlines():
            raw = raw.strip()
            if not raw:
                continue
            cleaned = re.sub(r'^\s*\d+\.\s*', '', raw)
            cleaned = cleaned.rstrip('.').strip()
            items.append(cleaned)
        return items

    def get_knowledge(self, profession):
        return self._clean_numbered_lines(profession.knowledge)

    def get_skills(self, profession):
        return self._clean_numbered_lines(profession.skills)

    def get_tags(self, profession):
        try:
            return json.loads(profession.tags)
        except Exception:
            return profession.tags if isinstance(profession.tags, (list,tuple)) else []

    def get_description(self, profession):
        desc = profession.description or ''
        return desc.rstrip('.').strip()
