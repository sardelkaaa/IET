from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserProfessionUpdateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/me/profession/', UserProfessionUpdateAPIView.as_view(), name='user-profession'),
]