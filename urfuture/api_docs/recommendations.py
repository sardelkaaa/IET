from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from recommendations.serializers import BestCourseSerializer

recommendations_list_response = OpenApiResponse(
    response=BestCourseSerializer(many=True),
    description='Топ 5 рекомендуемых курсов для пользователя по весу рекомендаций'
)

recommendations_list_examples = [
    OpenApiExample(
        name='Топ‑5 курсов пользователя',
        value=[
            {
                "course_id": 188,
                "course": "Разработка web-приложений на готовых платформах (CMS)",
                "discipline": "Прикладное программирование",
                "semester": 4,
                "weight": 8
            },
            {
                "course_id": 206,
                "course": "Fullstack-разработка на Next.JS",
                "discipline": "Профессиональный курс. Спецкурс 1",
                "semester": 5,
                "weight": 7
            },
            {
                "course_id": 174,
                "course": "JavaScript углублённый курс (SkillBox, смешанный)",
                "discipline": "Прикладное программирование",
                "semester": 4,
                "weight": 7
            },
            {
                "course_id": 178,
                "course": "Архитектура клиентских приложений на JS (HTML-академия)",
                "discipline": "Прикладное программирование",
                "semester": 4,
                "weight": 7
            },
            {
                "course_id": 246,
                "course": "Fullstack-разработка на Next.JS",
                "discipline": "Профессиональный курс. Спецкурс 4",
                "semester": 6,
                "weight": 7
            }
        ],
        response_only=True,
    ),
    OpenApiExample(
        name='Меньше 5, если рекомендаций мало',
        value=[
            {
                "course_id": 206,
                "course": "Fullstack-разработка на Next.JS",
                "discipline": "Профессиональный курс. Спецкурс 1",
                "semester": 5,
                "weight": 7
            }
        ],
        response_only=True,
    ),
]

recommendations_list_schema = extend_schema(
    summary='Список лучших курсов',
    description=(
        'Возвращает для текущего пользователя топ 5 курсов по дисциплинам, '
        'отсортированных по убыванию веса рекомендации.'
    ),
    responses={200: recommendations_list_response},
    examples=recommendations_list_examples,
)


best_courses_by_discipline_params = [
    OpenApiParameter(
        name='semester',
        description='Номер семестра для фильтрации рекомендаций',
        required=False,
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='profession',
        description='ID профессии, для которой строим рекомендации. '
                    'Если не указан — берётся профессия текущего пользователя',
        required=False,
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
    ),
]

best_courses_by_discipline_response = OpenApiResponse(
    response=BestCourseSerializer(many=True),
    description='Рекомендации лучших курсов разбитые по семестрам и дисциплинам',
)

best_courses_by_discipline_examples = [
    OpenApiExample(
        name='1. Все семестры (без фильтра)',
        value=[
            {
                "semester": 1,
                "courses": [
                    {"discipline": "Программирование",
                        "course": "Python. Базовый курс", "weight": 10},
                    {"discipline": "Физика",         "course": None,
                        "weight": None},
                ]
            },
            {
                "semester": 2,
                "courses": [
                    {"discipline": "Алгебра",
                        "course": "Линейная алгебра",        "weight": 8},
                    {"discipline": "Химия",          "course": None,
                        "weight": None},
                ]
            },
            {
                "semester": 3,
                "courses": [
                    {"discipline": "История",        "course": None,
                        "weight": None}
                ]
            }
        ],
        response_only=True,
    ),
    OpenApiExample(
        name='2. Фильтр по семестру',
        value=[
            {"discipline": "Алгебра", "course": "Линейная алгебра", "weight": 8},
            {"discipline": "Химия",   "course": None,               "weight": None},
        ],
        response_only=True,
    ),
    OpenApiExample(
        name='3. Для заданной профессии',
        value=[
            {
                "semester": 1,
                "courses": [
                    {"discipline": "Программирование",
                        "course": "Python. Базовый курс", "weight": 10},
                    {"discipline": "Физика",         "course": None,
                        "weight": None},
                ]
            },
            {
                "semester": 2,
                "courses": [
                    {"discipline": "Алгебра",
                        "course": "Линейная алгебра",        "weight": 8},
                    {"discipline": "Химия",          "course": None,
                        "weight": None},
                ]
            },
        ],
        response_only=True,
    ),
    OpenApiExample(
        name='404 — профессия не найдена',
        value={"detail": "No Profession matches the given query."},
        status_codes=["404"],
    ),
]

best_courses_by_discipline_schema = extend_schema(
    summary='Рекомендации лучших курсов для дисциплин',
    description=(
        'Возвращает для каждого семестра список дисциплин и '
        'рекомендуемых курсов (по убыванию веса). \n'
        '- Если передан `semester` в query — возвращает список '
        'без вложенной группировки по семестрам. \n'
        '- Если передан `profession` — строит рекомендации для указанной профессии, '
        'иначе — для профессии текущего пользователя.'
    ),
    parameters=best_courses_by_discipline_params,
    responses={
        200: best_courses_by_discipline_response,
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Профессия с таким ID не найдена'
        )
    },
    examples=best_courses_by_discipline_examples,
)
