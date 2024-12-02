import os
from dotenv import load_dotenv
from supabase import create_client, Client


def init_db():
    """Инициализация БД."""
    load_dotenv()
    return create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))


def print_recommended_courses_with_related_records(profession_data, profession_name, discipline_name=None):
    """Выводит на экран все подходящие курсы для профессии или дисциплины по убыванию веса."""
    if discipline_name:
        print(f'Дисциплина: {discipline_name}')
    else:
        print(f'Профессия: {profession_name}')

    if profession_data:
        for record in profession_data:
            print(f"Курс: {record['courses']['name']}, Компетенция: {record['competencies']['name']}, Вес: {record['weight']}")
    else:
        print('Рекомендованных курсов нет')

def print_top_recommended_courses_for_disciplines(top_courses, semester=None):
    semester = 'Все' if not semester else semester
    print(f'Лучшие курсы для выбранных дисциплин (семестр: {semester})')
    for discipline_name, (course_name, weight) in top_courses.items():
        if weight is not None:
            print(f'{discipline_name}: {course_name}, вес: {weight}')
        else:
            print(f'{discipline_name}: {course_name}')


def get_available_disciplines(supabase, direction_id, semester=None):
    """Получение доступных дисциплин для направления по семестрам."""
    discipline_links = supabase.table('disciplines-directions').select('discipline_id').eq('direction_id', direction_id)
    if semester:
        discipline_links = discipline_links.eq('semester', semester)
    # Возвращаем список из id дисциплин
    return [link['discipline_id'] for link in discipline_links.execute().data]


def recommend_courses(supabase, profession_id, direction_id):
    """Рекомендует курсы для профессии."""
    # Получаем доступные дисциплины для направления
    available_discipline_ids = get_available_disciplines(supabase, direction_id)

    # Теперь проверяем, что дисциплина у курса нам доступна для выбора(связана с направлением)
    profession_data = supabase.table('profession_competency_course_links').select(
        'professions(name), courses(name), competencies(name), weight, discipline_id'
    ).eq('profession_id', profession_id).in_('discipline_id', available_discipline_ids).execute().data

    profession_name = supabase.table('professions').select('*').eq('id', profession_id).execute().data[0]['name']

    print_recommended_courses_with_related_records(profession_data, profession_name)

def recommend_courses_within_discipline(supabase, profession_id, discipline_id, direction_id):
    """Рекомендует курсы для профессии в рамках конкретной дисциплины."""
    available_discipline_ids = get_available_disciplines(supabase, direction_id)
    if discipline_id not in available_discipline_ids:
        print(f'Дисциплина с id {discipline_id} недоступна для направления с id {direction_id}')
        return

    profession_data = supabase.table('profession_competency_course_links').select(
        'courses(name), competencies(name), weight'
    ).eq('profession_id', profession_id).eq('discipline_id', discipline_id).execute().data

    profession_name = supabase.table('professions').select('name').eq('id', profession_id).execute().data[0]['name']
    discipline_name = supabase.table('disciplines').select('name').eq('id', discipline_id).execute().data[0]['name']

    print_recommended_courses_with_related_records(profession_data, profession_name, discipline_name)


def get_top_recommended_courses_for_disciplines(supabase, profession_id, direction_id, discipline_ids, semester=None):
    """Получение самого рекомендуемого курса для каждой дисциплины из списка по семестрам."""
    # Получаем список доступных дисциплин для направления по семестрам
    available_discipline_ids = get_available_disciplines(supabase, direction_id, semester)

    # Ограничиваем переданные дисциплины так, чтобы они были связаны с направлением и указанным семестром
    valid_discipline_ids = [discipline_id for discipline_id in discipline_ids if discipline_id in available_discipline_ids]

    if not valid_discipline_ids:
        print(f'Выбранные дисциплины недоступны в рамках направления и семестра: {semester}')
        return

    response = supabase.table('disciplines').select('id, name').in_('id', valid_discipline_ids).execute()

    disciplines = {
        discipline['id']: discipline['name']
        for discipline in response.data
    }

    top_courses = {}

    for discipline_id in valid_discipline_ids:
        profession_data = supabase.table('profession_competency_course_links').select(
            'courses(name), weight'
        ).eq('profession_id', profession_id).eq('discipline_id', discipline_id).limit(1).execute().data

        if profession_data:
            top_course = profession_data[0]['courses']['name']
            top_weight = profession_data[0]['weight']
            top_courses[disciplines[discipline_id]] = (top_course, top_weight)
        else:
            top_courses[disciplines[discipline_id]] = ('Нет рекомендованных курсов', None)

    print_top_recommended_courses_for_disciplines(top_courses, semester)



def get_disciplines_for_direction(supabase, direction_id, semester=None):
    """Получение всех дисциплин в рамках направления по семестрам"""

    available_discipline_ids = get_available_disciplines(supabase, direction_id, semester)

    response = supabase.table('disciplines').select('name').in_('id', available_discipline_ids).execute()
    disciplines = [discipline['name'] for discipline in response.data]
    semester = 'Все' if not semester else semester

    print(f'Дисциплины в рамках выбранного направления (семестр: {semester}):')
    for discipline in disciplines:
        print(f'Название: {discipline}')

    return available_discipline_ids


# Тестируем функцию
def main():
    supabase = init_db()
    profession_id = int(input('Id of the profession: '))
    discipline_id = int(input('Id of the discipline: '))
    direction_id = int(input('Id of the direction: '))

    semester = int(input('Id of the semester: '))

    recommend_courses(supabase, profession_id, direction_id)
    print()

    recommend_courses_within_discipline(supabase, profession_id, discipline_id, direction_id)
    print()

    discipline_ids = [86, 72, 82, 5]
    get_top_recommended_courses_for_disciplines(supabase, profession_id, direction_id, discipline_ids)
    print()

    all_disciplines_for_direction = get_disciplines_for_direction(supabase, direction_id, semester)
    print()

    get_top_recommended_courses_for_disciplines(supabase, profession_id, direction_id, all_disciplines_for_direction, semester)


if __name__ == '__main__':
    main()