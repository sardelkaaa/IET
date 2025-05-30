from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer, ProfessionSelectSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api_docs.users import register_schema, login_schema, refresh_schema, profile_schema, user_profile_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import caches


@register_schema
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        cache = caches['default']
        cache.delete_pattern('*user_profile*')
        cache.delete_pattern('*user_profession*')
        cache.delete_pattern('*best_courses*')
        cache.delete_pattern('*best_courses_by_discipline*')


@login_schema
class LoginAPIView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        cache = caches['default']
        cache.delete_pattern('*user_profile*')
        cache.delete_pattern('*user_profession*')
        cache.delete_pattern('*best_courses*')
        cache.delete_pattern('*best_courses_by_discipline*')
        return response


@refresh_schema
class MyTokenRefreshView(TokenRefreshView):
    pass


@profile_schema
@method_decorator(cache_page(60 * 60 * 24, key_prefix='user_profession'), name='get')
class UserProfessionUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionSelectSerializer
    http_method_names = ['get', 'patch', 'options', 'head']

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        cache = caches['default']
        cache.delete_pattern('*user_profession*')
        cache.delete_pattern('*best_courses*')
        cache.delete_pattern('*best_courses_by_discipline*')


@method_decorator(cache_page(60 * 60 * 24, key_prefix='user_profile'), name='dispatch')
@user_profile_schema
class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
