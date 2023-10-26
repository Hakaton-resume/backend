from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import StudentViewSet, VacancyViewSet, TagViewSet, SkillViewSet

app_name = 'api'

v1_router = SimpleRouter()

v1_router.register(r'students', StudentViewSet, basename='students')
v1_router.register(r'vacancies', VacancyViewSet, basename='vacancies')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'skills', SkillViewSet, basename='skills')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
