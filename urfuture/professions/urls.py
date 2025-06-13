from django.urls import path
from .views import ProfessionListAPIView, ProfessionDetailAPIView

urlpatterns = [
    path('', ProfessionListAPIView.as_view(), name='professions-list'),
    path('<int:pk>/', ProfessionDetailAPIView.as_view(), name='profession-detail')
]