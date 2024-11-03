# Алгоритм для произвольной БД с построением связей
# Компетенция - курс и курс - компетенция

import os
from dotenv import load_dotenv
from supabase import *

def get_common_tags(tags1, tags2): # вынес формирование общих тегов в отдельную функцию
    common_tags = set(tags1).intersection(tags2)
    return list(common_tags), len(common_tags)

def get_linking_profession_to_competency(profession, data_of_competencies):
    matched_competencies = []
    for competency in data_of_competencies:
        common_tags, weight = get_common_tags(profession[0]['tags'], competency['tags']) # везде было с ['tags'] а тут нет
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
    matched_courses = []
    for course in list_of_courses: # поменял переменную на course
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
                } # Добавлены недостающие атрибуты
            )
    return matched_courses

def recommend_courses(profession, competencies, courses, discipline=None): # по умолчанию будем обозначать, что фильтра нет
    matched_competencies = get_linking_profession_to_competency(profession, competencies)
    all_matched_courses = []
    for competency in matched_competencies:
        matched_courses = get_linking_competency_to_course(competency, courses)

        if discipline: # если был передан фильтр(на данный момент на принадлежность курсов дисциплине)
            matched_courses = list(filter(lambda x: x['discipline_id'] == discipline, matched_courses)) # проверяем, что в данной дисциплине есть ссылка на id курса
        for match_course in matched_courses:
            match_course['weight'] += competency['weight']
        all_matched_courses.extend(matched_courses)
    return sorted(all_matched_courses, key=lambda x: x['weight'], reverse=True)

def recommend_courses_for_profession(profession, competencies, courses):
    return recommend_courses(profession, competencies, courses)

# В рамках дисциплины должны выбрать наиболее подходящий из связанных с ней курсов
def recommend_course_for_discipline(profession, competencies, courses, discipline):
    return recommend_courses(profession, competencies, courses, discipline=discipline)

def init_db(): # Инициализация БД
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


# professions = {
#     1: {'name': 'Data Scientist', 'tags': ['python', 'statistics', 'machine learning', 'programming basics', 'data analysis']},
#     2: {'name': 'Web Developer', 'tags': ['html', 'css', 'javascript', 'react']},
#     3: {'name': 'Backend Go Developer', 'tags': ['go']}
# }
#
# competencies = {
#     1: {'name': 'Python Programming', 'tags': ['python', 'data analysis']},
#     2: {'name': 'Frontend Development', 'tags': ['html', 'css', 'javascript']},
#     3: {'name': 'Backend Development', 'tags': ['database']},
#     4: {'name': 'Base Programming', 'tags': ['programming basics']},
#     5: {'name': 'Data Science', 'tags': ['machine learning', 'statistics', 'data analysis']},
# }
#
# courses = {
#     1: {'name': 'Introduction to Python', 'tags': ['programming basics'], 'discipline_id': None},
#     2: {'name': 'Advanced Web Development', 'tags': ['javascript', 'react', 'html'], 'discipline_id': 1},
#     3: {'name': 'Data Science Course', 'tags': ['python', 'machine learning', 'statistics', 'data analysis'], 'discipline_id': 1},
# }
#
# disciplines = {
#     1: {'name': 'Современные языки программирования'}
# }
#

# Тестируем функцию

def main():
    supabase = init_db()

    profession_id = int(input('Id of the profession: '))
    discipline_id = int(input('Id of the discipline: '))

    professions = supabase.table('professions').select('*')
    profession = professions.eq('id', profession_id).execute().data  # Алгоритм поиска профессии по id в таблице

    disciplines = supabase.table('disciplines').select('*')
    discipline = disciplines.eq('id', discipline_id).execute().data # Алгоритм поиска дисциплины по id в таблице

    competencies = supabase.table('competencies').select('*').execute().data
    courses = supabase.table('courses').select('*').execute().data

    recommended_courses = recommend_courses_for_profession(profession, competencies, courses)

    # Выводим список рекомендованных курсов
    print(f'Профессия: {profession[0]['name']}')

    for recommended_course in recommended_courses:
        print(f"Компетенция: {recommended_course['competency']['name']}, Курс: {recommended_course['name']}, Вес: {recommended_course['weight']}")
    print()

    discipline_courses = recommend_course_for_discipline(profession, competencies, courses, discipline)

    print(f'Дисциплина: {discipline[0]['name']}')
    for discipline_course in discipline_courses:
        print(f"Курс: {discipline_course['name']} в рамках компетенции {discipline_course['competency']['name']} с весом {discipline_course['weight']}")

if __name__ == '__main__':
    main()