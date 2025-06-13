from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiExample, extend_schema
from drf_spectacular.types import OpenApiTypes
from disciplines.serializers import DisciplineSerializer

disciplines_list_params = [
    OpenApiParameter(
        name='semester',
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description='Номер семестра для фильтрации дисциплин',
        required=False,
    ),
]

disciplines_list_response = OpenApiResponse(
    response=DisciplineSerializer,
    description='Список дисциплин с полем semester',
)


discipline_list_examples = [
    OpenApiExample(
        name='All disciplines',
        value=[
            {
                "id": 71,
                "name": "Прикладная физическая культура",
                "semester": 1
            },
            {
                "id": 73,
                "name": "Программирование",
                "semester": 1
            },
            {
                "id": 82,
                "name": "История",
                "semester": 1
            },
            {
                "id": 91,
                "name": "Информационные технологии и сервисы",
                "semester": 1
            },
            {
                "id": 102,
                "name": "Дискретная математика",
                "semester": 2
            },
            {
                "id": 113,
                "name": "Алгоритмы и структуры данных",
                "semester": 2
            },
            {
                "id": 124,
                "name": "Философия",
                "semester": 3
            },
            {
                "id": 135,
                "name": "Экономика",
                "semester": 3
            }
        ]
    ),
    OpenApiExample(
        name='Semester 2 only',
        value=[
            {
                "id": 102,
                "name": "Дискретная математика",
                "semester": 2
            },
            {
                "id": 113,
                "name": "Алгоритмы и структуры данных",
                "semester": 2
            }
        ]
    )
]

disciplines_list_doc = extend_schema(
    summary='Дисциплины направления пользователя',
    description=(
        'Возвращает все дисциплины для направления пользователя'
        '- Если параметр `semester` не передан — отдаёт полный список с полем `semester`.\n'
        '- Если передан — только дисциплины указанного семестра'
    ),
    parameters=disciplines_list_params,
    responses={200: disciplines_list_response},
    examples=discipline_list_examples
)
