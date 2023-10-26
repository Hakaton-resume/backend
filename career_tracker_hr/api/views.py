from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from career.models import Favourite, Vacancy, Skill, Tag, Resp
from users.models import StudentUser, Company
from api.serializers import (VacancySerializer, StudentSerializer,
                             FavouriteSerializer, VacancyCandidateSerializer,
                             SkillSerializer, TagSerializer,
                             VacancyCreateSerializer, StudentSerializer,
                             CompanySerializer)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',) 


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    #permission_classes = (IsAdminOrReadOnly,)
    #filter_backends = (SearchFilter,)
    #search_fields = ('^name',)        


class StudentViewSet(ModelViewSet):
    queryset = StudentUser.objects.all()
    serializer_class = StudentSerializer

    @action(
        detail=True,
        methods=['post'],
        url_path='favourites/(?P<vacancy_id>\d+)'
    )
    def to_favorite(self, request, pk=None, vacancy_id=None):
        """Добавить студента в избранное вакансии"""
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        student = get_object_or_404(StudentUser, id=pk)
        Favourite.objects.create(vacancy=vacancy, student=student)
        serializer = StudentSerializer(
                student, context={'request': request}
            )
        return Response(serializer.data, status=HTTP_201_CREATED)


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()

    @action(
        detail=True,
    )
    def favourites(self, request, pk=None):
        """Просмотреть список избранных"""
        vacancy = get_object_or_404(Vacancy, id=pk)
        serializer = VacancySerializer(vacancy, context={'request': request})
        return Response(serializer.data)


    @action(detail=True,
            # permission_classes=[IsAuthenticated]
    )
    def candidates(self, request, pk):
        """Возвращает два списка кандидатов"""
        vacancy = get_object_or_404(Vacancy, id=pk)
        candidates = Resp.objects.filter(vacancy=vacancy)
        students = [candidate.student for candidate in candidates]
        serializer = StudentSerializer(
                students, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return VacancySerializer
        elif self.action == 'candidates':
            return StudentSerializer
        return VacancyCreateSerializer
