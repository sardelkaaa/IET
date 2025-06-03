from django.urls import path
from .views import RegisterAPIView, LoginAPIView, MyTokenRefreshView, UserProfessionUpdateAPIView, UserProfileAPIView, UserProfileUpdateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('users/me/profession/', UserProfessionUpdateAPIView.as_view(), name='user-profession'),
    path('users/me/update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('users/me/', UserProfileAPIView.as_view(), name='user-profile'),
]
