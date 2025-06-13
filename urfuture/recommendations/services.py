from .models import ProfessionCompetencyCourseLink
from disciplines.services import get_available_disciplines


def recommend_courses(profession_id, direction_id):
    """
    Рекомендует курсы для профессии.
    """
    available_disciplines = get_available_disciplines(direction_id)
    recommended_courses = ProfessionCompetencyCourseLink.objects.filter(
        profession__id=profession_id,
        discipline__in=available_disciplines
    ).select_related('course', 'competency', 'discipline')
    return recommended_courses


def recommend_courses_within_discipline(profession_id, discipline_id, direction_id):
    """
    Рекомендует курсы для профессии в рамках конкретной дисциплины.
    """
    available_disciplines = get_available_disciplines(direction_id)
    if not available_disciplines.filter(id=discipline_id).exists():
        return None

    recommended_courses = ProfessionCompetencyCourseLink.objects.filter(
        profession__id=profession_id,
        discipline__id=discipline_id
    ).select_related('course', 'competency')
    return recommended_courses


def get_top_recommended_courses_for_disciplines(profession_id, direction_id, discipline_ids, semester=None):
    """
    Получение самого рекомендуемого курса для каждой дисциплины.
    """
    available_disciplines = get_available_disciplines(direction_id, semester)
    valid_discipline_ids = available_disciplines.filter(id__in=discipline_ids).values_list('id', flat=True)

    top_courses = {}

    recommended_courses = ProfessionCompetencyCourseLink.objects.filter(
        profession__id=profession_id,
        discipline__id__in=valid_discipline_ids
    ).select_related('discipline', 'course')

    for record in recommended_courses:
        if record.discipline.id not in top_courses:
            top_courses[record.discipline.name] = (record.course.name, record.weight)

    for discipline_id in valid_discipline_ids:
        discipline = available_disciplines.get(id=discipline_id)
        if discipline.name not in top_courses:
            top_courses[discipline.name] = ('Нет рекомендованных курсов', None)

    return top_courses
