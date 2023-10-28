from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        PrimaryKeyRelatedField, ImageField)

from career.models import Favourite, Vacancy, Skill, Tag, Resp, Invitation
from users.models import StudentUser, Company
from api.serializers import (VacancySerializer, StudentSerializer,
                             SkillSerializer, TagSerializer,
                             VacancyCreateSerializer, StudentSerializer, VacancyCreateFavouriteSerializer,
                             CompanySerializer, VacancyResponseSerializer,
                             VacancyFavouriteSerializer, VacancyInvitationSerializer)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
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


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()

    @action(
        detail=True,
        methods=['post'],
        url_path='favourites/(?P<student_id>\d+)'
    )
    def to_favourite(self, request, pk=None, student_id=None):
        """Добавить студента в избранное вакансии"""
        vacancy = get_object_or_404(Vacancy, id=student_id)
        student = get_object_or_404(StudentUser, id=pk)
        Favourite.objects.create(vacancy=vacancy, student=student)
        serializer = VacancyCreateFavouriteSerializer(
                vacancy, context={'request': request}
            )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def response(self, request, pk=None):
        vacancy = self.get_object()
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def favourites(self, request, pk=None):
        vacancy = self.get_object()
        serializer = VacancyFavouriteSerializer(
            vacancy,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def invitations(self, request, pk=None):
        vacancy = self.get_object()
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return VacancySerializer
        if self.action == 'response':
            return VacancyResponseSerializer
        elif self.action == 'invitations':
            return VacancyInvitationSerializer
        elif self.action == 'favourites':
            return VacancyFavouriteSerializer
        elif self.action == 'to_favourite':
            return VacancyCreateFavouriteSerializer
        elif self.request.method == 'POST':
            return VacancyCreateSerializer
