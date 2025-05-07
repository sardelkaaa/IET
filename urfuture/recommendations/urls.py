from django.urls import path
from .views import BestCoursesByDisciplineAPIView, BestCoursesAPIView

urlpatterns = [
    path('', BestCoursesAPIView.as_view(), name='recommendations-list'),
    path('by-discipline/', BestCoursesByDisciplineAPIView.as_view(), name='recommendations-by-discipline'),
]