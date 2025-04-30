from django.urls import path
from .views import DirectionListAPIView

urlpatterns = [
    path('', DirectionListAPIView.as_view(), name='directions-list'),
]