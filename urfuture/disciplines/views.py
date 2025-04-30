from rest_framework import generics
from .models import DisciplinesDirections
from .serializers import DisciplineSerializer


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
