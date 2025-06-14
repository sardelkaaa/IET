from django.db.models import OuterRef, Subquery, F
from disciplines.models import DisciplinesDirections
from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.models import ProfessionCompetencyCourseLink as PCCL
from professions.models import Profession
from rest_framework import status
from api_docs.recommendations import recommendations_list_schema, best_courses_by_discipline_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 60 * 24, key_prefix='best_courses_by_discipline'), name='dispatch')
@best_courses_by_discipline_schema
class BestCoursesByDisciplineAPIView(APIView):
    def get(self, request):
        user = request.user
        prof_param = request.query_params.get('profession')
        if prof_param is not None:
            try:
                profession = int(prof_param)
            except ValueError:
                return Response(
                    {"detail": "Invalid profession ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not Profession.objects.filter(id=profession).exists():
                return Response(
                    {"detail": "Profession not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            profession = user.profession_id
        direction = user.direction_id
        semester = request.query_params.get('semester')
        if not profession or not direction:
            return Response([])

        dd_qs = DisciplinesDirections.objects.filter(direction_id=direction) \
            .select_related('discipline')
        if semester is not None:
            dd_qs = dd_qs.filter(semester=int(semester))

        best_link = PCCL.objects.filter(
            profession_id=profession,
            discipline_id=OuterRef('discipline_id')
        ).order_by('-weight')

        results = dd_qs.annotate(
            course_name=Subquery(best_link.values('course__name')[:1]),
            weight=Subquery(best_link.values('weight')[:1])
        )

        if semester is not None:
            data = [
                {
                    "discipline": dd.discipline.name,
                    "discipline_category": dd.discipline.category,
                    "course":     dd.course_name,
                    "weight":     dd.weight
                }
                for dd in results
            ]
            data.sort(key=lambda x: (-(x["weight"] or 0), x["discipline"]))
            return Response(data)

        grouped = {}
        for dd in results:
            sem = dd.semester
            grouped.setdefault(sem, []).append({
                "discipline": dd.discipline.name,
                "discipline_category": dd.discipline.category,
                "course":     dd.course_name,
                "weight":     dd.weight
            })
        response = []
        for sem in sorted(grouped):
            items = grouped[sem]
            items.sort(key=lambda x: (-(x["weight"] or 0), x["discipline"]))
            response.append({"semester": sem, "courses": items})
        return Response(response)


@method_decorator(cache_page(60 * 60 * 24, key_prefix='best_courses'), name='dispatch')
@recommendations_list_schema
class BestCoursesAPIView(APIView):
    def get(self, request):
        user = request.user
        profession = user.profession_id
        direction = user.direction_id

        if not profession or not direction:
            return Response([])

        qs = (
            PCCL.objects
            .filter(
                profession_id=profession,
                discipline__disciplinesdirections__direction_id=direction
            )
            .annotate(
                semester=F('discipline__disciplinesdirections__semester')
            )
            .select_related('course', 'discipline')
            .order_by('-weight')[:5]
        )

        data = [
            {
                "course_id":  rec.course.id,
                "course":     rec.course.name,
                "discipline": rec.discipline.name,
                "semester":   rec.semester,
                "weight":     rec.weight,
            }
            for rec in qs
        ]

        return Response(data)
