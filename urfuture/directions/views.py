from rest_framework import generics, permissions
from .models import Direction
from .serializers import DirectionSerializer
from api_docs.directions import directions_list_schema, directions_detail_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 60 * 24, key_prefix='directions_list'), name='dispatch')
@directions_list_schema
class DirectionListAPIView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = (permissions.AllowAny,)


@method_decorator(cache_page(60 * 60 * 24, key_prefix='direction_detail'), name='dispatch')
@directions_detail_schema
class DirectionDetailAPIView(generics.RetrieveAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = (permissions.AllowAny,)
