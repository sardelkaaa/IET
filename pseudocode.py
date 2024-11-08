# Алгоритм для произвольной БД с построением связей
# Компетенция - курс и курс - компетенция

import os
from dotenv import load_dotenv
from supabase import create_client, Client


def get_common_tags(tags1, tags2):
    """Получение общих тегов из двух списков с тегами."""
    if tags1 and tags2:
        common_tags = set(tags1).intersection(tags2)
        return list(common_tags), len(common_tags)
    return [], 0


def get_linking_profession_to_competency(profession, data_of_competencies):
    """Получение связанных профессий и компетенций."""
    matched_competencies = []
    for competency in data_of_competencies:
        common_tags, weight = get_common_tags(profession['tags'], competency['tags'])
        if common_tags:
            matched_competencies.append(
                {
                    'id': competency['id'],
                    'name': competency['name'],
                    'tags': competency['tags'],
                    'weight': weight
                }
            )
    return matched_competencies


def get_linking_competency_to_course(competency, list_of_courses):
    """Получение связанных компетенций и курсов."""
    matched_courses = []
    for course in list_of_courses:
        common_tags, weight = get_common_tags(competency['tags'], course['tags'])
        if common_tags:
            matched_courses.append(
                {
                    'id': course['id'],
                    'name': course['name'],
                    'description': course['description'],
                    'knowledge': course['knowledge'],
                    'skills': course['skills'],
                    'discipline_id': course['discipline_id'],
                    'direction_id': course['direction_id'],
                    'competency': competency,
                    'tags': course['tags'],
                    'weight': weight
                }
            )
    return matched_courses


def recommend_courses(profession, competencies, courses, discipline_id=None):
    """Рекомендация курсов."""
    matched_competencies = get_linking_profession_to_competency(profession, competencies)
    all_matched_courses = []
    for competency in matched_competencies:
        matched_courses = get_linking_competency_to_course(competency, courses)

        if discipline_id:  # если был передан фильтр принадлежности курсов дисциплине, то оставляем только курсы связанные с дисциплиной
            matched_courses = list(filter(lambda x: x['discipline_id'] == discipline_id, matched_courses))
        for match_course in matched_courses:
            match_course['weight'] += competency['weight']
        all_matched_courses.extend(matched_courses)
    return sorted(all_matched_courses, key=lambda x: x['weight'], reverse=True)


def recommend_courses_for_profession(profession, competencies, courses):
    return recommend_courses(profession, competencies, courses)


def recommend_course_for_discipline(profession, competencies, courses, discipline_id=None):
    """Рекомендация курсов для профессии."""
    return recommend_courses(profession, competencies, courses, discipline_id=discipline_id)


def get_top_recommended_course_for_disciplines(discipline_ids, profession, competencies, courses, supabase):
    """Получение самого рекомендуемого курса для каждой дисциплины из списка."""
    top_courses = {}
    for discipline_id in discipline_ids:
        discipline_courses = recommend_course_for_discipline(profession, competencies, courses, discipline_id)
        discipline = supabase.table('disciplines').select('name').eq('id', discipline_id).execute().data[0]

        if discipline_courses:
            top_course = discipline_courses[0]
            top_courses[discipline['name']] = top_course['name']
        else:
            top_courses[discipline['name']] = 'Нет рекомендованных курсов'

    for discipline_name, course_name in top_courses.items():
        print(f'{discipline_name}: {course_name}')


def init_db():
    """Инициализация БД."""
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


def get_entity_by_name(supabase, table_name):
    """Делает поиск сущностей и их id в базе данных."""
    search = input(f'Введите данные для поиска в таблице {table_name}: ')
    response = (supabase.table(table_name)
                    .select('id, name')
                    .ilike('name', f"%{search}%")
                    .execute())
    if response.data:
        for search in sorted(response.data, key=lambda x: x['id']):
            print(search)
    else:
        print('Не найдено в базе данных')


def print_recommended_courses(profession_name, courses, discipline_name=None):
    """Выводит на экран все подходящие курсы для профессии или дисциплины по убыванию веса."""
    if discipline_name:
        print(f'Дисциплина: {discipline_name}')
    else:
        print(f'Профессия: {profession_name}')

    if courses:
        for course in courses:
            print(f"Курс: {course['name']}, Компетенция: {course['competency']['name']}, Вес: {course['weight']}")
    else:
        print('Рекомендованных курсов нет')


# Тестируем функцию
def main():
    supabase = init_db()
    get_entity_by_name(supabase, 'professions')
    profession_id = int(input('Id of the profession: '))
    get_entity_by_name(supabase, 'disciplines')
    discipline_id = int(input('Id of the discipline: '))

    # Алгоритм поиска профессии по id в таблице
    profession = supabase.table('professions').select('*').eq('id', profession_id).execute().data[0]

    # Алгоритм поиска дисциплины по id в таблице
    discipline = supabase.table('disciplines').select('*').eq('id', discipline_id).execute().data[0]

    competencies = supabase.table('competencies').select('*').execute().data
    courses = supabase.table('courses').select('*').execute().data

    recommended_courses = recommend_courses_for_profession(profession, competencies, courses)
    discipline_courses = recommend_course_for_discipline(profession, competencies, courses, discipline_id)

    # Выводим список рекомендованных курсов
    print_recommended_courses(profession['name'], recommended_courses)
    print()
    # Выводим список рекомендованных курсов в рамках дисциплины
    print_recommended_courses(profession['name'], discipline_courses, discipline['name'])

    print()

    # тестовую профессию можно взять с id 123
    discipline_ids = [8, 14, 32]
    get_top_recommended_course_for_disciplines(discipline_ids, profession, competencies, courses, supabase)


if __name__ == '__main__':
    main()
