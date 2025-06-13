from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from api_docs.schema import HiddenSchemaView
from drf_spectacular.views import (
    SpectacularSwaggerView, SpectacularRedocView
)

urlpatterns = [
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/professions/', include('professions.urls')),
    path('api/directions/', include('directions.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/disciplines/', include('disciplines.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/schema/', HiddenSchemaView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/',  include('users.urls')),
]
