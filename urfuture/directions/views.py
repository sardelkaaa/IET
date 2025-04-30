from rest_framework import generics, permissions
from .models import Direction
from .serializers import DirectionSerializer


class DirectionListAPIView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = (permissions.AllowAny,)
