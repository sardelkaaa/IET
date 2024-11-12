from pseudocode import init_db, recommend_courses_for_profession


def get_table_with_related_records():
    """Заполнение таблицы profession_competency_course_links данными о связях"""
    supabase = init_db()

    professions = supabase.table('professions').select('*').execute().data
    competencies = supabase.table('competencies').select('*').execute().data
    courses = supabase.table('courses').select('*').execute().data

    data = [
        {
            'profession_id': course['profession_id'],
            'competency_id': course['competency_id'],
            'course_id': course['course_id'],
            'weight': course['weight'],
            'discipline_id': course['discipline_id']
        }
        for profession in professions
        for course in recommend_courses_for_profession(profession, competencies, courses)
    ]

    try:
        response = supabase.table('profession_competency_course_links').insert(data).execute()
        return response

    except Exception as exception:
        return exception

if __name__ == '__main__':
    get_table_with_related_records()