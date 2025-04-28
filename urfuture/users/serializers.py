from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

Student = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    patronymic = serializers.CharField(required=True, allow_blank=False, max_length=150)
    email = serializers.EmailField(
        write_only=True,
        validators=[UniqueValidator(queryset=Student.objects.all())]
    )

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'direction', 'password', 'access', 'refresh')

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
