from django.urls import path
from .views import MyDirectionDisciplinesAPIView

urlpatterns = [
    path('', MyDirectionDisciplinesAPIView.as_view(), name='disciplines-by-direction'),
]