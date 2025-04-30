from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/professions/', include('professions.urls')),
    path('api/directions/', include('directions.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/disciplines/', include('disciplines.urls')),
    path('api/',  include('users.urls'))
]
