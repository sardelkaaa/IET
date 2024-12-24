from .models import DisciplinesDirections, Disciplines


def get_available_disciplines(direction_id, semester=None):
    """
    Получение доступных дисциплин для указанного направления с учетом семестра.
    """
    disciplines_directions = DisciplinesDirections.objects.filter(direction__id=direction_id)
    if semester:
        disciplines_directions = disciplines_directions.filter(semester=semester)
    
    # Извлекаем дисциплины, связанные с направлением
    discipline_ids = disciplines_directions.values_list('discipline_id', flat=True)
    return Disciplines.objects.filter(id__in=discipline_ids)


def get_disciplines_for_direction(direction_id, semester=None):
    """
    Получение всех дисциплин в рамках направления по семестрам.
    """
    disciplines = get_available_disciplines(direction_id, semester)
    return disciplines.values_list('name', flat=True)
