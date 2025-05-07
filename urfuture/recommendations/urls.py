from django.urls import path
from .views import BestCoursesByDisciplineAPIView

urlpatterns = [
    path('best-courses/by-discipline/', BestCoursesByDisciplineAPIView.as_view(), name='best-courses'),
]