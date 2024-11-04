# Алгоритм для произвольной БД с построением связей
# Компетенция - курс и курс - компетенция

import os
from dotenv import load_dotenv
from supabase import create_client, Client


def get_common_tags(tags1, tags2):
    """Получение общих тегов из двух списков с тегами."""
    common_tags = set(tags1).intersection(tags2)
    return list(common_tags), len(common_tags)


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


def recommend_courses(profession, competencies, courses, discipline=None):
    """Рекомендация курсов."""
    matched_competencies = get_linking_profession_to_competency(profession, competencies)
    all_matched_courses = []
    for competency in matched_competencies:
        matched_courses = get_linking_competency_to_course(competency, courses)

        if discipline:  # если был передан фильтр принадлежности курсов дисциплине, то оставляем только курсы связанные с дисциплиной
            matched_courses = list(filter(lambda x: x['discipline_id'] == discipline, matched_courses))
        for match_course in matched_courses:
            match_course['weight'] += competency['weight']
        all_matched_courses.extend(matched_courses)
    return sorted(all_matched_courses, key=lambda x: x['weight'], reverse=True)


def recommend_courses_for_profession(profession, competencies, courses):
    """Рекомендация курсов для профессии."""
    return recommend_courses(profession, competencies, courses)


def recommend_course_for_discipline(profession, competencies, courses, discipline):
    """Рекомендация курсов в рамках дисциплины."""
    return recommend_courses(profession, competencies, courses, discipline=discipline)


def init_db():
    """Инициализация БД."""
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


def get_profession_by_name(supabase):
    """Делает поиск профессий и их id в базе данных."""
    profession = input('Введите имя профессии: ')
    response = (supabase.table('professions')
                    .select('id, name')
                    .ilike('name', f"%{profession}%")
                    .execute())
    if response.data:
        for profession in response.data:
            print(profession)
    else:
        print('Профессия не найдена в базе данных')


# Тестируем функцию
def main():
    supabase = init_db()
    get_profession_by_name(supabase)
    profession_id = int(input('Id of the profession: '))
    discipline_id = int(input('Id of the discipline: '))

    # Алгоритм поиска профессии по id в таблице
    profession = supabase.table('professions').select('*').eq('id', profession_id).execute().data[0]

    # Алгоритм поиска дисциплины по id в таблице
    discipline = supabase.table('disciplines').select('*').eq('id', discipline_id).execute().data[0]

    competencies = supabase.table('competencies').select('*').execute().data
    courses = supabase.table('courses').select('*').execute().data

    recommended_courses = recommend_courses_for_profession(profession, competencies, courses)

    # Выводим список рекомендованных курсов
    print(f'Профессия: {profession['name']}')

    if recommended_courses:
        for recommended_course in recommended_courses:
            print(f"Компетенция: {recommended_course['competency']['name']}, Курс: {recommended_course['name']}, Вес: {recommended_course['weight']}")
    else:
        print('В базе данных нет рекомендованных курсов для выбранной профессии')
    print()

    discipline_courses = recommend_course_for_discipline(profession, competencies, courses, discipline)

    print(f'Дисциплина: {discipline['name']}')
    if discipline_courses:
        for discipline_course in discipline_courses:
            print(f"Компетенция: {discipline_course['name']}, Курс: {discipline_course['competency']['name']}, Вес: {discipline_course['weight']}")
    else:
        print('В базе данных нет рекомендованных курсов для выбранной профессии в рамках выбранной дисциплины')


if __name__ == '__main__':
    main()