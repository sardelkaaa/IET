from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from users.serializers import RegisterSerializer, ProfessionSelectSerializer, UserProfileSerializer, UserProfileUpdateSerializer

register_req = OpenApiExample(
    'Register request',
    summary='Тело запроса для регистрации пользователя',
    request_only=True,
    value={
        "first_name": "string",
        "last_name": "string",
        "patronymic": "string",
        "email": "user@example.com",
        "direction": 0,
        "password": "string"
    }
)

register_resp_201 = OpenApiExample(
    'Register success',
    summary='Успешная регистрация, возвращает данные пользователя + токены',
    response_only=True,
    value={
        "id": 0,
        "first_name": "string",
        "last_name": "string",
        "patronymic": "string",
        "direction": 0,
        "access": "string",
        "refresh": "string"
    }
)

register_resp_400 = OpenApiExample(
    'Register failure',
    summary='Ошибка валидации данных',
    response_only=True,
    value={
        "password": ["Ensure this field has at least 8 characters."],
        "email": ["This field must be unique."]
    }
)

register_schema = extend_schema(
    summary='Регистрация нового пользователя',
    description=(
        'Создаёт нового пользователя и возвращает его данные вместе с JWT-токенами.\n'
        '- Поле `password` должно быть не менее 8 символов\n'
        '- Поле `email` должно быть уникальным'
    ),
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=RegisterSerializer,
            description='Пользователь успешно зарегистрирован',
            examples=[register_resp_201],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Ошибка валидации при регистрации',
            examples=[register_resp_400],
        ),
    },
    auth=[],
    examples=[register_req],
    tags=['auth'],
)


login_req = OpenApiExample(
    'Login request',
    summary='Тело запроса для получения JWT‑токенов',
    request_only=True,
    value={
        "email": "user@example.com",
        "password": "string"
    }
)

login_resp_200 = OpenApiExample(
    'Login success',
    summary='Успешный ответ: refresh + access',
    response_only=True,
    value={
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…"
    }
)

login_resp_401 = OpenApiExample(
    'Login failure',
    summary='Ошибка аутентификации',
    response_only=True,
    value={
        "detail": "No active account found with the given credentials"
    }
)

login_schema = extend_schema(
    summary='Авторизация (JWT login)',
    description=(
        'Возвращает пару JWT-токенов:\n'
        '- `access` — для доступа к защищённым эндпоинтам\n'
        '- `refresh` — для обновления `access`'
    ),
    request=TokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairSerializer,
            description='Успешно получены токены',
            examples=[login_resp_200],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Неверные учётные данные',
            examples=[login_resp_401],
        ),
    },
    examples=[login_req],
    tags=['auth'],
)


refresh_req = OpenApiExample(
    'Refresh token request',
    summary='Тело запроса для обновления access-токена',
    request_only=True,
    value={
        "refresh": "string"
    }
)

refresh_resp_200 = OpenApiExample(
    'Refresh success',
    summary='Успешный ответ: новый access-токен',
    response_only=True,
    value={
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.…"
    }
)

refresh_resp_401 = OpenApiExample(
    'Refresh failure',
    summary='Невалидный или просроченный refresh-токен',
    response_only=True,
    value={
        "detail": "Token is invalid or expired"
    }
)

refresh_schema = extend_schema(
    summary='Обновление JWT‑токена',
    description=(
        'Принимает JSON с полем `refresh` и возвращает новый `access`‑токен. '
        'Поле `refresh` должно быть действительным и не просроченным.'
    ),
    request=TokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshSerializer,
            description='Новый access-токен успешно сгенерирован',
            examples=[refresh_resp_200],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Невалидный или просроченный refresh-токен',
            examples=[refresh_resp_401],
        ),
    },
    examples=[refresh_req],
    tags=['auth'],
)

profession_get_example = OpenApiExample(
    'Profession detail',
    summary='Текущая профессия пользователя',
    response_only=True,
    value={
        "profession": 4,
        "profession_name": "Web-программист"
    }
)

profile_resp_400 = OpenApiExample(
    'Profile update validation error',
    summary='Ошибка валидации при обновлении профессии',
    response_only=True,
    value={
        "profession": ["A valid integer is required."]
    }
)

profile_resp_401 = OpenApiExample(
    'Unauthorized error',
    summary='Неавторизованный запрос',
    response_only=True,
    value={
        "detail": "Authentication credentials were not provided."
    }
)

profile_schema = extend_schema(
    summary='Просмотр и изменение профессии пользователя',
    description='Позволяет получить текущую профессию или обновить ее.',
    tags=["user profession"],
    request={
        'PATCH': ProfessionSelectSerializer
    },
    responses={
        200: OpenApiResponse(
            response=ProfessionSelectSerializer,
            description='Данные профиля',
            examples=[profession_get_example],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Ошибки в запросе при обновлении',
            examples=[profile_resp_400],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Неавторизованный',  
            examples=[profile_resp_401],    
        ),
    },
)

user_profile_example = OpenApiExample(
    'User profile',
    summary='Данные профиля пользователя',
    response_only=True,
    value={
        "id": 1,
        "last_name": "Иванов",
        "first_name": "Петр",
        "patronymic": "Сергеевич",
        "email": "ivanov@urfu.me",
        "academic_group": "ИТС-2023",
        "direction": "Программная инженерия",
        "direction_id": 4,
    }
)

user_profile_401 = OpenApiExample(
    'Unauthorized error',
    summary='Неавторизованный запрос',
    response_only=True,
    value={
        "detail": "Authentication credentials were not provided."
    }
)

user_profile_schema = extend_schema(
    summary='Получение данных профиля',
    description=(
        'Возвращает основные данные текущего авторизованного пользователя:\n'
        '- ФИО\n'
        '- Основной email\n'
        '- Академическая группа\n'
        'Для доступа требуется JWT-токен в заголовке Authorization'
    ),
    responses={
        200: OpenApiResponse(
            response=UserProfileSerializer,
            description='Данные профиля',
            examples=[user_profile_example],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Неавторизованный доступ',
            examples=[user_profile_401],
        ),
    },
    methods=['GET'],
    tags=['user profile'],
)

update_profile_example = OpenApiExample(
    'User profile update',
    summary='Данные профиля после успешного обновления',
    response_only=True,
    value={
        "id": 1,
        "last_name": "Иванов",
        "first_name": "Петр",
        "patronymic": "Сергеевич",
        "email": "ivanov@urfu.me",
        "academic_group": "ИТС-2023",
        "direction": "Программная инженерия",
        "direction_id": 4,
    }
)

user_profile_400_example = OpenApiExample(
    'Profile update validation error',
    summary='Ошибки валидации при обновлении профиля',
    response_only=True,
    value={
        "email": ["Enter a valid email address."],
        "new_password": ["This password is too short."],
    }
)

user_profile_update_schema = extend_schema(
    summary='Обновление данных профиля',
    description=(
        'Позволяет обновить поля профиля и при необходимости сменить пароль.\n'
        'Для смены пароля передайте `current_password`, `new_password`, `new_password_confirm`.\n'
        'Для доступа требуется JWT-токен.'
    ),
    request=UserProfileUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=UserProfileSerializer,
            description='Данные профиля после успешного обновления',
            examples=[update_profile_example],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Ошибки валидации при обновлении профиля',
            examples=[user_profile_400_example],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Неавторизованный доступ',
            examples=[user_profile_401],
        ),
    },
    methods=['PATCH'],
    tags=['user profile'],
)
