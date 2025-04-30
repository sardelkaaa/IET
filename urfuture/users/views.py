from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer, ProfessionSelectSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LoginAPIView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class UserProfessionUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionSelectSerializer

    def get_object(self):
        return self.request.user
