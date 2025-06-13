from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from professions.serializers import ProfessionSerializer, ProfessionDetailSerializer

professions_list_examples = [
    OpenApiExample(
        name="Пример списка",
        value=[
            {"id": 1, "name": "Инженер-схемотехник"},
            {"id": 2, "name": "Программист высокопроизводительных вычислительных систем"},
            {"id": 3, "name": "Специалист по искусственному интеллекту"},
            {"id": 4, "name": "Web‑программист"},
        ],
    ),
]

professions_list_schema = extend_schema(
    summary="Список профессий",
    description="Возвращает список всех доступных профессий.",
    responses={
        200: OpenApiResponse(
            response=ProfessionSerializer(many=True),
            description="Список объектов Profession",
        )
    },
    examples=professions_list_examples,
    auth=[]
)

professions_detail_examples = [
    OpenApiExample(
        name="Подробная информация",
        value={
            "id": 12,
            "name": "Информатик‑технолог",
            "description": "Информатик‑технолог – это специалист, занимающийся созданием, администрированием и обслуживанием информационных технологий в различных сферах. В его обязанности входят: ...",
            "knowledge": [
                "Информационные технологии: глубокие знания в области ИТ, включая программирование, базы данных, сети и безопасность",
                "Программирование: знание языков Python, Java или C++ для разработки технологических решений",
                "Системный анализ: понимание методов системного анализа для исследования и улучшения бизнес‑процессов",
                "Технологии обработки данных: знание SQL, NoSQL, Big Data и машинного обучения",
                "Проектное управление: принципы управления проектами, планирование, оценка рисков и управление ресурсами"
            ],
            "skills": [
                "Аналитическое мышление: способность анализировать сложные системы и выявлять возможности для оптимизации",
                "Решение проблем: умение идентифицировать и решать технические и бизнес‑проблемы",
                "Коммуникация: эффективно общаться с разными заинтересованными сторонами",
                "Командная работа: работать над проектами в составе междисциплинарных команд",
                "Обучаемость: готовность быстро осваивать новые технологии и методологии"
            ],
            "tags": ["Информационные технологии", "Python", "MATLAB", "Системный анализ", "Автоматизация"]
        },
        response_only=True,
    ),
]

professions_detail_not_found_example = OpenApiExample(
    name="Профессия не найдена",
    summary="404 при отсутствии профессии",
    description="Возвращается, если в базе нет профессии с таким ID",
    value={"detail": "No Profession matches the given query."},
    status_codes=["404"],
    response_only=True,
)

professions_detail_schema = extend_schema(
    summary="Подробная информация о профессии",
    description="Возвращает все поля профессии: описание, знания, навыки и теги.",
    parameters=[
        OpenApiParameter(
            name="id",
            location=OpenApiParameter.PATH,
            required=True,
            type=OpenApiTypes.INT,
            description="ID профессии"
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=ProfessionDetailSerializer,
            description="Детальный объект Profession",
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Профессия с таким ID не найдена",
            examples=[professions_detail_not_found_example]
        ),
    },
    examples=professions_detail_examples,
    auth=[]
)