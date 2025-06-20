from rest_framework import generics, permissions
from .models import Profession
from .serializers import ProfessionSerializer, ProfessionDetailSerializer
from api_docs.professions import professions_list_schema, professions_detail_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination


class ProfessionsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


@method_decorator(cache_page(60 * 60 * 24, key_prefix='professions_list'), name='dispatch')
@professions_list_schema
class ProfessionListAPIView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = ProfessionsPagination

    def get_queryset(self):
        queryset = Profession.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


@method_decorator(cache_page(60 * 60 * 24, key_prefix='professions_list_no_pagination'), name='dispatch')
class ProfessionListNoPaginationAPIView(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


@method_decorator(cache_page(60 * 60 * 24, key_prefix='profession_detail'), name='dispatch')
@professions_detail_schema
class ProfessionDetailAPIView(generics.RetrieveAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionDetailSerializer
    permission_classes = (permissions.AllowAny,)
