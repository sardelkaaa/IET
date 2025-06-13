from rest_framework import generics, permissions
from django.db.models import Min, Max, Q
from api_docs.courses import courses_list_schema, course_detail_schema
from .models import Course
from .serializers import CourseSerializer, CourseDetailSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination


class CoursesPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 30


@method_decorator(cache_page(60 * 60 * 24, key_prefix='courses_list'), name='dispatch')
@courses_list_schema
class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = CoursesPagination

    def get_queryset(self):
        user = self.request.user
        direction_id = getattr(user, 'direction_id', None)
        if not direction_id:
            return Course.objects.none()

        qs = Course.objects.filter(
            Q(directions__contains=[direction_id]) |
            Q(directions__isnull=True,
              discipline__disciplinesdirections__direction_id=direction_id)
        )

        qs = qs.annotate(
            min_sem=Min(
                'discipline__disciplinesdirections__semester',
                filter=Q(
                    discipline__disciplinesdirections__direction_id=direction_id)
            ),
            max_sem=Max(
                'discipline__disciplinesdirections__semester',
                filter=Q(
                    discipline__disciplinesdirections__direction_id=direction_id)
            )
        )

        semester = self.request.query_params.get('semester')
        if semester is not None:
            try:
                sem = int(semester)
                qs = qs.filter(
                    discipline__disciplinesdirections__direction_id=direction_id,
                    discipline__disciplinesdirections__semester=sem
                )
            except ValueError:
                return Course.objects.none()

        return qs.select_related('discipline').distinct().order_by('id')


@method_decorator(cache_page(60 * 60 * 24, key_prefix='course_detail'), name='dispatch')
@course_detail_schema
class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.AllowAny,)
