from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from professions.models import Profession
from django.contrib.auth.password_validation import validate_password

Student = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    patronymic = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        write_only=True,
        validators=[UniqueValidator(queryset=Student.objects.all())]
    )

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'direction', 'password', 'access', 'refresh')

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = Student(email=email, **validated_data)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)
        validated_data = {
            'access':  str(refresh.access_token),
            'refresh': str(refresh)
        }
        user._tokens = validated_data
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        tokens = getattr(instance, '_tokens', {})
        data.update(tokens)
        return data


class ProfessionSelectSerializer(serializers.ModelSerializer):
    profession = serializers.PrimaryKeyRelatedField(
        queryset=Profession.objects.all(),
        required=True,
        help_text='ID выбранной профессии'
    )
    profession_name = serializers.CharField(
        source='profession.name',
        read_only=True,
        help_text='Название выбранной профессии'
    )

    class Meta:
        model = Student
        fields = ('profession', 'profession_name')


class UserProfileSerializer(serializers.ModelSerializer):
    direction = serializers.CharField(
        source='direction.name_text',
        read_only=True,
        help_text="Направление"
    )
    direction_id = serializers.PrimaryKeyRelatedField(
        source='direction',
        read_only=True,
        help_text="ID направления"
    )
    profession = serializers.CharField(
        source='profession.name',
        read_only=True,
        help_text="Выбранная профессия"
    )
    profession_id = serializers.PrimaryKeyRelatedField(
        source='profession',
        read_only=True,
        help_text="ID профессии"
    )

    class Meta:
        model = Student
        fields = (
            'id',
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'profession_id',
            'profession',
            'direction_id',
            'direction',
            'academic_group'
        )
        read_only_fields = ('email',)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False)
    academic_group = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(required=False)

    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'academic_group',
            'email',
            'current_password',
            'new_password',
            'new_password_confirm',
        )

    def validate_email(self, value):
        user = self.context['request'].user
        if Student.objects.exclude(pk=user.pk).filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate(self, attrs):
        user = self.context['request'].user

        current = attrs.get('current_password')
        new = attrs.get('new_password')
        confirm = attrs.get('new_password_confirm')

        if current or new or confirm:
            if not current or not new or not confirm:
                raise serializers.ValidationError("Для смены пароля нужно заполнить все три поля: текущий пароль, новый пароль и подтверждение")

            if not user.check_password(current):
                raise serializers.ValidationError({"current_password": "Текущий пароль неверен"})

            if new != confirm:
                raise serializers.ValidationError({"new_password_confirm": "Новый пароль и подтверждение не совпадают"})

        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.academic_group = validated_data.get('academic_group', instance.academic_group)
        instance.email = validated_data.get('email', instance.email)

        new_password = validated_data.get('new_password', None)
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance
