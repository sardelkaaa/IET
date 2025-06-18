from rest_framework import generics
from .models import DisciplinesDirections
from .serializers import DisciplineSerializer
from api_docs.disciplines import disciplines_list_doc
from rest_framework.response import Response


@disciplines_list_doc
class MyDirectionDisciplinesAPIView(generics.ListAPIView):
    serializer_class = DisciplineSerializer

    def get_queryset(self):
        user = self.request.user
        direction_id = getattr(user, 'direction_id', None)
        if not direction_id:
            return DisciplinesDirections.objects.none()

        qs = DisciplinesDirections.objects.filter(direction_id=direction_id)
        semester = self.request.query_params.get('semester')
        if semester:
            qs = qs.filter(semester=semester)
        return qs.select_related('discipline').order_by('semester')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        grouped = {}
        for item in data:
            sem = item['semester']
            entry = {
                'id': item['id'],
                'name': item['name'],
                'category': item['category']
            }
            grouped.setdefault(sem, []).append(entry)

        result = [
            {'semester': sem, 'courses': courses}
            for sem, courses in sorted(grouped.items(), key=lambda x: x[0])
        ]

        return Response(result)
