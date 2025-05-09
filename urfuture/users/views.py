from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer, ProfessionSelectSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api_docs.users import register_schema, login_schema, refresh_schema, profile_schema


@register_schema
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


@login_schema
class LoginAPIView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


@refresh_schema
class MyTokenRefreshView(TokenRefreshView):
    pass


@profile_schema
class UserProfessionUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionSelectSerializer
    http_method_names = ['get', 'put', 'options', 'head']

    def get_object(self):
        return self.request.user
