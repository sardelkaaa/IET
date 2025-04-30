from django.urls import path
from .views import BestCoursesAPIView

urlpatterns = [
    path('best-courses/', BestCoursesAPIView.as_view(), name='best-courses'),
]