from django.db.models import OuterRef, Subquery
from disciplines.models import DisciplinesDirections
from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.models import ProfessionCompetencyCourseLink as PCCL


class BestCoursesByDisciplineAPIView(APIView):
    def get(self, request):
        user = request.user
        profession = user.profession_id
        direction = user.direction_id
        semester = request.query_params.get('semester')
        if not profession or not direction:
            return Response([])

        dd_qs = DisciplinesDirections.objects.filter(direction_id=direction)
        if semester is not None:
            dd_qs = dd_qs.filter(semester=int(semester))
        dd_qs = dd_qs.select_related('discipline')

        best_link = PCCL.objects.filter(
            profession_id=profession,
            discipline_id=OuterRef('discipline_id')
        ).order_by('-weight')

        results = dd_qs.annotate(
            course_name=Subquery(best_link.values('course__name')[:1]),
            weight=Subquery(best_link.values('weight')[:1])
        )

        # Build JSON response
        if semester is not None:
            # single semester: flat list
            data = [
                {
                    "discipline": dd.discipline.name,
                    "course":     dd.course_name,
                    "weight":     dd.weight
                }
                for dd in results
            ]
            data.sort(key=lambda x: (-(x["weight"] or 0), x["discipline"]))
            return Response(data)

        # multi-semester: group by semester
        grouped = {}
        for dd in results:
            sem = dd.semester
            grouped.setdefault(sem, []).append({
                "discipline": dd.discipline.name,
                "course":     dd.course_name,
                "weight":     dd.weight
            })
        response = []
        for sem in sorted(grouped):
            items = grouped[sem]
            items.sort(key=lambda x: (-(x["weight"] or 0), x["discipline"]))
            response.append({"semester": sem, "courses": items})
        return Response(response)
