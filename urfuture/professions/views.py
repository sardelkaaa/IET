from rest_framework import generics, permissions
from .models import Profession
from .serializers import ProfessionSerializer, ProfessionDetailSerializer


class ProfessionListAPIView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = (permissions.AllowAny,)


class ProfessionDetailAPIView(generics.RetrieveAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionDetailSerializer
    permission_classes = (permissions.AllowAny,)
