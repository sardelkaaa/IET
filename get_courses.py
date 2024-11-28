import os
from dotenv import load_dotenv
from supabase import create_client, Client


def init_db():
    """Инициализация БД."""
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


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


def get_available_disciplines(supabase, direction_id):
    """Получение доступных дисциплин для направления."""
    discipline_links = supabase.table('disciplines-directions').select('discipline_id').eq('direction_id', direction_id).execute().data
    # Возвращем просто список из id дисциплин
    return [link['discipline_id'] for link in discipline_links]


def recommend_courses(supabase, profession_id, direction_id):
    """Рекомендует курсы для профессиия."""
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
        print(f'Дисциплина с id {discipline_id} не доступна для направления с id {direction_id}')
        return

    profession_data = supabase.table('profession_competency_course_links').select(
        'courses(name), competencies(name), weight'
    ).eq('profession_id', profession_id).eq('discipline_id', discipline_id).execute().data

    profession_name = supabase.table('professions').select('name').eq('id', profession_id).execute().data[0]['name']
    discipline_name = supabase.table('disciplines').select('name').eq('id', discipline_id).execute().data[0]['name']

    print_recommended_courses_with_related_records(profession_data, profession_name, discipline_name)


def get_top_recommended_courses_for_disciplines(supabase, profession_id, direction_id, discipline_ids):
    """Получение самого рекомендуемого курса для каждой дисциплины из списка."""
    # Получаем список доступных дисциплин для направления
    available_discipline_ids = get_available_disciplines(supabase, direction_id)

    # Ограничиваем переданные дисциплины так, чтобы они были связаны с направлением
    valid_discipline_ids = [discipline_id for discipline_id in discipline_ids if discipline_id in available_discipline_ids]

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

    print('Лучшие курсы для выбранных дисциплин:')
    for discipline_name, course_data in top_courses.items():
        course_name, weight = course_data
        if weight is not None:
            print(f'{discipline_name}: {course_name}, вес: {weight}')
        else:
            print(f'{discipline_name}: {course_name}')


# Тестируем функцию
def main():
    supabase = init_db()
    profession_id = int(input('Id of the profession: '))
    discipline_id = int(input('Id of the discipline: '))
    direction_id = int(input('Id of the direction: '))

    recommend_courses(supabase, profession_id, direction_id)
    print()

    recommend_courses_within_discipline(supabase, profession_id, discipline_id, direction_id)
    print()

    discipline_ids = [8, 14, 32]
    get_top_recommended_courses_for_disciplines(supabase, profession_id, direction_id, discipline_ids)


if __name__ == '__main__':
    main()