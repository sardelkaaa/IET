from django.urls import path
from .views import ProfessionListAPIView, ProfessionDetailAPIView, ProfessionListNoPaginationAPIView

urlpatterns = [
    path('', ProfessionListAPIView.as_view(), name='professions-list'),
    path('all/', ProfessionListNoPaginationAPIView.as_view(), name='professions-list-no-pagination'),
    path('<int:pk>/', ProfessionDetailAPIView.as_view(), name='profession-detail')
]