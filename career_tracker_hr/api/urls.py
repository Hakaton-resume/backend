from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import StudentViewSet

app_name = 'api'

v1_router = SimpleRouter()

v1_router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
