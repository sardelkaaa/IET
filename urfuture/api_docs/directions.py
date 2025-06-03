from drf_spectacular.utils import OpenApiResponse, OpenApiExample, extend_schema
from directions.serializers import DirectionSerializer

directions_response = OpenApiResponse(
    response=DirectionSerializer(many=True),
    description="Список всех доступных направлений"
)

directions_list_schema = extend_schema(
    summary="Получить список направлений",
    description=(
        "Возвращает все направления (например, 09.03.01, 09.03.02 и т.д.), "
        "доступные для выбора студентом."
    ),
    auth=[],
    responses={200: directions_response},
    examples=[
        OpenApiExample(
            name='',
            summary='Реальный пример',
            value=[
                {'id': 1, 'name': '09.03.01', 'description': 'Описание ИВТ', 'name_text': 'Информатика и вычислительная техника'},
                {'id': 2, 'name': '09.03.03', 'description': 'Описание Прикладной информатики', 'name_text': 'Прикладная информатика'},
                {'id': 3, 'name': '09.03.04', 'description': 'Описание Программной инженерии', 'name_text': 'Программная инженерия'},
            ],
        )
    ]
)
