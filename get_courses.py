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


def recommend_courses(supabase, profession_id):
    """Рекомендует курсы для профессии."""
    # Получение курсов по id профессии
    profession_data = supabase.table('profession_competency_course_links').select(
        'professions(name), courses(name), competencies(name), weight').eq('profession_id', profession_id).execute().data

    profession_name = supabase.table('professions').select('*').eq('id', profession_id).execute().data[0]['name']

    print_recommended_courses_with_related_records(profession_data, profession_name)


def recommend_courses_within_discipline(supabase, profession_id, discipline_id):
    """Рекомендует курсы для профессии в рамках конкретной дисциплины."""
    profession_data = supabase.table('profession_competency_course_links').select(
        'courses(name), competencies(name), weight'
    ).eq('profession_id', profession_id).eq('discipline_id', discipline_id).execute().data

    profession_name = supabase.table('professions').select('name').eq('id', profession_id).execute().data[0]['name']
    discipline_name = supabase.table('disciplines').select('name').eq('id', discipline_id).execute().data[0]['name']

    print_recommended_courses_with_related_records(profession_data, profession_name, discipline_name)


def get_top_recommended_courses_for_disciplines(supabase, profession_id, discipline_ids):
    """Получение самого рекомендуемого курса для каждой дисциплины из списка."""

    # Изначально выбираем только те дисциплины, где есть совпадения по id из списка discipline_ids
    response = supabase.table('disciplines').select('id, name').in_('id', discipline_ids).execute()
    disciplines = {
        discipline['id']: discipline['name']
        for discipline in response.data
    }

    top_courses = {}
    for discipline_id in discipline_ids:
        # Получаем курсы для заданной профессии и дисциплины
        profession_data = supabase.table('profession_competency_course_links').select(
            'courses(name), weight'
        ).eq('profession_id', profession_id).eq('discipline_id', discipline_id
        ).limit(1).execute().data

        if profession_data:
            top_course = profession_data[0]['courses']['name']
            top_courses[disciplines[discipline_id]] = top_course
        else:
            top_courses[disciplines[discipline_id]] = 'Нет рекомендованных курсов'

    print('Лучшие курсы для выбранных дисциплин:')
    for discipline_name, course_name in top_courses.items():
        print(f'{discipline_name}: {course_name}')


# Тестируем функцию
def main():
    supabase = init_db()
    profession_id = int(input('Id of the profession: '))
    discipline_id = int(input('Id of the discipline: '))
    recommend_courses(supabase, profession_id)
    print()
    recommend_courses_within_discipline(supabase, profession_id, discipline_id)
    print()
    discipline_ids = [8, 14, 32]
    get_top_recommended_courses_for_disciplines(supabase, profession_id, discipline_ids)


if __name__ == '__main__':
    main()
