from django.urls import path
from .views import DirectionListAPIView, DirectionDetailAPIView

urlpatterns = [
    path('', DirectionListAPIView.as_view(), name='directions-list'),
    path('<int:pk>/', DirectionDetailAPIView.as_view(), name='direction-detail')
]