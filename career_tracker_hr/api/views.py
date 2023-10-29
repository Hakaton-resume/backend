from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        PrimaryKeyRelatedField, ImageField)
from django.http import HttpResponse

from career.models import Vacancy, Skill, Tag, Favourite, Invitation, Resp
from users.models import StudentUser, Company
from api.serializers import (VacancyResponseSerializer, StudentSerializer, InvitationSerializer,
                             SkillSerializer, TagSerializer, ResponseSerializer,
                             VacancyCreateSerializer, StudentSerializer, VacancySerializer,
                             CompanySerializer, VacancyAllSerializer, FavouriteSerializer,
                             VacancyFavouriteSerializer, VacancyInvitationSerializer)
from api.utils import download_file
from api.filters import SkillFilter, TagFilter


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('^name',)
    filterset_class = TagFilter


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('^name',)
    filterset_class = SkillFilter


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    #permission_classes = (IsAdminOrReadOnly,)


class StudentViewSet(ModelViewSet):
    queryset = StudentUser.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)

    @action(detail=True)
    def download_cv(self, request, pk=None):
        """Загрузить резюме"""
        cv = self.get_object().cv
        if cv:
            return download_file(cv)
        else:
            return Response(
                {'detail': 'Резюме не найдено'},
                status=HTTP_404_NOT_FOUND
            )


    @action(detail=True)
    def download_portfolio(self, request, pk=None):
        """Загрузить портфолио"""
        portfolio = self.get_object().portfolio
        if portfolio:
            return download_file(portfolio)
        else:
            return Response(
                {'detail': 'Портфолио не было загружено пользователем'},
                status=HTTP_404_NOT_FOUND
            )


class VacancyCreateViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favourites/(?P<student_id>\d+)'
    )
    def to_favourite(self, request, pk=None, student_id=None):
        """Добавить студента в избранное вакансии или удалить"""
        vacancy = get_object_or_404(Vacancy, pk=pk)
        student = get_object_or_404(StudentUser, pk=student_id)
        if request.method == 'POST':
            if Favourite.objects.filter(
                vacancy=vacancy, student=student
            ).exists():
                return Response(
                    {'errors': 'Студент уже добавлен в избранное'},
                    status=HTTP_400_BAD_REQUEST
                )
            Favourite.objects.create(
                vacancy=vacancy, student=student
            )
            serializer = VacancyFavouriteSerializer(
                vacancy, context={'request': request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
                
        if request.method == 'DELETE':
            favourite = Favourite.objects.filter(
                vacancy=vacancy, student=student
            )
            if favourite.exists():
                favourite.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Студента не было в избранном вакансии'},
                    status=HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete'],
        url_path='response/(?P<student_id>\d+)'
    )
    def del_response(self, request, pk=None, student_id=None):
        """Удалить студента из откликов"""
        vacancy = get_object_or_404(Vacancy, pk=pk)
        student = get_object_or_404(StudentUser, pk=student_id)
        response = Resp.objects.filter(
                vacancy=vacancy, student=student
            )
        if response.exists():
            response.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'Студент не откликался на вакансии'},
                status=HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post'],
        url_path='invitations/(?P<student_id>\d+)'
    )
    def to_invitation(self, request, pk=None, student_id=None):
        """Пригласить на собеседование"""
        vacancy = get_object_or_404(Vacancy, pk=pk)
        student = get_object_or_404(StudentUser, pk=student_id)
        if Invitation.objects.filter(
            vacancy=vacancy, student=student
        ).exists():
            return Response(
                {'errors': 'Студент уже приглашен'},
                status=HTTP_400_BAD_REQUEST
            )
        Invitation.objects.create(
            vacancy=vacancy, student=student
        )
        if Favourite.objects.filter(
            vacancy=vacancy, student=student
        ).exists():
            Favourite.objects.filter(
                vacancy=vacancy, student=student
            ).delete()
        if Resp.objects.filter(
            vacancy=vacancy, student=student
        ).exists():
            Resp.objects.filter(
                vacancy=vacancy, student=student
            ).delete()
        serializer = VacancyInvitationSerializer(
            vacancy, context={'request': request}
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=True)
    def groups(self, request, pk=None):
        vacancy = self.get_object()
        serializer = VacancyAllSerializer(
            vacancy,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def response(self, request, pk=None):
        vacancy = self.get_object()
        responses = Resp.objects.filter(vacancy=vacancy)
        serializer = ResponseSerializer(
            responses,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True)
    def favourites(self, request, pk=None):
        vacancy = self.get_object()
        favourites = Favourite.objects.filter(vacancy=vacancy)
        serializer = FavouriteSerializer(
            favourites,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def invitations(self, request, pk=None):
        vacancy = self.get_object()
        invitations = Invitation.objects.filter(vacancy=vacancy)
        serializer = InvitationSerializer(
            invitations,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'response':
            return ResponseSerializer
        elif self.action == ('invitations', 'to_invitation'):
            return InvitationSerializer
        elif self.action in ('favourites', 'to_favourite'):
            return FavouriteSerializer
        elif self.action == 'groups':
            return VacancyAllSerializer
        elif self.action == 'list' or self.action == 'retrieve':
            return VacancySerializer
        return VacancyCreateSerializer
