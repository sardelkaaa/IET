from rest_framework import generics, permissions
from .models import Direction
from .serializers import DirectionSerializer
from api_docs.directions import directions_list_schema


@directions_list_schema
class DirectionListAPIView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = (permissions.AllowAny,)
