from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CompanyViewSet, StudentViewSet, VacancyViewSet, TagViewSet, SkillViewSet, VacancyCreateViewSet

app_name = 'api'

v1_router = SimpleRouter()

v1_router.register(r'students', StudentViewSet, basename='students')
v1_router.register(r'vacancies', VacancyViewSet, basename='vacancies')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'skills', SkillViewSet, basename='skills')
v1_router.register(r'companies', CompanyViewSet, basename='companies')
#v1_router.register(r'responses', ResponseViewSet, basename='responses')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
