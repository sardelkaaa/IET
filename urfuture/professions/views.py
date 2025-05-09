from rest_framework import generics, permissions
from .models import Profession
from .serializers import ProfessionSerializer, ProfessionDetailSerializer
from api_docs.professions import professions_list_schema, professions_detail_schema


@professions_list_schema
class ProfessionListAPIView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = (permissions.AllowAny,)


@professions_detail_schema
class ProfessionDetailAPIView(generics.RetrieveAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionDetailSerializer
    permission_classes = (permissions.AllowAny,)
