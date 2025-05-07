from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.models import ProfessionCompetencyCourseLink as PCCL


class BestCoursesAPIView(APIView):
    def get(self, request):
        user = request.user
        profession = user.profession_id
        direction = user.direction_id
        if not profession or not direction:
            return Response([])

        semester_param = request.query_params.get('semester')

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
            .order_by('discipline_id', '-weight')
            .distinct('discipline_id')
        )

        if semester_param:
            qs = qs.filter(
                discipline__disciplinesdirections__semester=semester_param
            )
            data = [
                {
                    "discipline": rec.discipline.name,
                    "course":     rec.course.name,
                    "weight":     rec.weight,
                }
                for rec in qs
            ]
            return Response(data)

        grouped = {}
        for rec in qs:
            sem = rec.semester
            grouped.setdefault(sem, []).append({
                "discipline": rec.discipline.name,
                "course":     rec.course.name,
                "weight":     rec.weight,
            })

        response = [
            {
                "semester": sem,
                "courses": items
            }
            for sem, items in sorted(grouped.items())
        ]
        return Response(response)
