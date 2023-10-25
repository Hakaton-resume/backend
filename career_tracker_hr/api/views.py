from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet


class StudentViewSet(ModelViewSet):
    pass


#class VacancyViewSet(ModelViewSet):
#    queryset = Vacancy.objects.all()
#    # permission_classes =
#
#    @action(detail=True,
#            methods=['post', 'delete']
#            # permission_classes=[IsAuthenticated]
#            )
#    def resp(self, request, id):
#        """Откликнуться на вакансию/отменить отклик"""
#        user = request.user
#        vacancy = get_object_or_404(Vacancy, id=id)
#
#        if request.method == 'POST':
#            if Resp.objects.filter(user=user, vacancy=vacancy).exists():
#                return Response(
#                    {'errors': 'Вы уже откликались на эту вакансию'},
#                    status=HTTP_400_BAD_REQUEST
#                )
#            resp = Resp.objects.create(user=user, vacancy=vacancy)
#            serializer = RespSerializer(
#                vacancy, context={'request': request}
#            )
#            return Response(serializer.data, status=HTTP_201_CREATED)
#
#        if request.method == 'DELETE':
#            resp = Resp.objects.filter(user=user, vacancy=vacancy)
#            if resp.exists():
#                resp.delete()
#                return Response(status=HTTP_204_NO_CONTENT)
#            return Response(
#                {'error': 'Вы не откликались на эту вакансию'},
#                status=HTTP_400_BAD_REQUEST
#            )
#    
#    @action(detail=True,
#            # permission_classes=[IsAuthenticated]
#    )
#    def candidates(self, request, id):
#        """Возвращает два списка кандидатов кандидатов"""
#       vacancy = get_object_or_404(Vacancy, id=id)
#        serializer = VacancySerializer(
#                vacancy, context={'request': request}
#        )
#        return self.get_paginated_response(serializer.data)
#
#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)
#
#    def perform_destroy(self, instance):
#        instance.image.delete()
#        instance.delete() 
