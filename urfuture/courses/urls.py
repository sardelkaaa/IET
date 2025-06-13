from django.urls import path
from .views import CourseListAPIView, CourseDetailAPIView

urlpatterns = [
    path('', CourseListAPIView.as_view(), name='courses-list'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail')
]
