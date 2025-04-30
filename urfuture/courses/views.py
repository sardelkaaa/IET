from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        direction_id = getattr(user, 'direction_id', None)
        if not direction_id:
            return Course.objects.none()

        return Course.objects.filter(directions__contains=[direction_id])
