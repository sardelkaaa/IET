from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from courses.serializers import CourseSerializer, CourseDetailSerializer

courses_list_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name='semester',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Фильтр курсов по семестру',
            required=False,
        ),
    ],
    responses=OpenApiResponse(
        response=CourseSerializer(many=True),
        examples=[
            OpenApiExample(
                'All courses',
                value=[
                    {
                        "id": 185,
                        "name": "Прикладное программирование на TypeScript (ArtSofte, RUS, TK)",
                        "discipline": "Прикладное программирование",
                        "semester": "4"
                    },
                    {
                        "id": 124,
                        "name": "Компьютерная арифметика",
                        "discipline": "Математические методы для разработчиков 3",
                        "semester": "7"
                    },
                    {
                        "id": 13,
                        "name": "Алгоритмы и структуры данных (SkillFactory, OK)",
                        "discipline": "Алгоритмы и анализ сложности",
                        "semester": "4"
                    }
                ],
                response_only=True,
                status_codes=['200'],
            ),
            OpenApiExample(
                'Semester 2 only',
                value=[
                    {
                        "id": 44,
                        "name": "Технологии «Фабрик Будущего» (онлайн, СПБПУ, ОК)",
                        "discipline": "Введение в инженерную деятельность",
                        "semester": "2"
                    },
                    {
                        "id": 342,
                        "name": "Философия: ключевые темы, проблемы, решения",
                        "discipline": "Философия",
                        "semester": "2"
                    }
                ],
                response_only=True,
                status_codes=['200'],
            ),
        ],
    ),
    tags=['courses'],
    summary="Список всех курсов для направления пользователя",
    description="Возвращает список курсов, дисциплину и семестр",
)

course_detail_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name='id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID курса',
            required=True,
        ),
    ],
    auth=[],
    responses={
        200: OpenApiResponse(
            response=CourseDetailSerializer,
            examples=[
                OpenApiExample(
                    'Course detail',
                    value={
                        "id": 185,
                        "name": "Прикладное программирование на TypeScript (ArtSofte, RUS, TK)",
                        "description": "Полное описание курса по прикладному программированию на TypeScript.",
                        "knowledge": [
                            "Основы TypeScript",
                            "Типизация",
                            "Работа с API"
                        ],
                        "skills": [
                            "Разработка на TypeScript",
                            "Дебаггинг",
                            "Тестирование"
                        ],
                        "tags": [
                            "программирование",
                            "TypeScript",
                            "frontend"
                        ]
                    },
                    response_only=True,
                    status_codes=['200'],
                ),
            ],
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Course not found.",
            examples=[
                OpenApiExample(
                    'Not found',
                    value={"detail": "No Course matches the given query."},
                    response_only=True,
                    status_codes=['404'],
                ),
            ],
        ),
    },
    tags=['courses'],
    summary="Подробная информация о курсе",
    description="Возвращает все поля курса: описание, знания, навыки и теги.",
)
