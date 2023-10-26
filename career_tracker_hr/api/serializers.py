from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        PrimaryKeyRelatedField)
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.utils import percentage_of_similarity
from career.models import Favourite, Vacancy, Resp, Tag, Skill
from users.models import StudentUser


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов вакансии"""

    class Meta:
        fields = '__all__'
        model = Tag


class SkillSerializer(ModelSerializer):
    """Сериализатор для навыков"""
    class Meta:
        fields = '__all__'
        model = Skill


class RespSerializer(ModelSerializer):
    """Сериализатор для откликов на вакансии"""

    class Meta:
        fields = '__all__'
        model = Resp


class FavouriteSerializer(ModelSerializer):

   class Meta:
       model = Favourite
       fields = '__all__'


class StudentSerializer(ModelSerializer):

   class Meta:
       model = StudentUser
       fields = '__all__'       


class VacancySerializer(ModelSerializer):
    
    class Meta:
        model = Vacancy
        fields = (
            'name',
            'company',
            'tags',
            'skills'
        )       


#class VacancySerializer(ModelSerializer):
#    favourites = SerializerMethodField()
#    
#    class Meta:
#        model = Vacancy
#        fields = (
#            'name',
#            'company',
#            'favourites'
#        )
#    
#    def get_favourites(self, obj):
#        request = self.context.get('request')
#        favourites = Favourite.objects.filter(vacancy=obj)
#        students = [favourite.student for favourite in favourites]
#        return StudentSerializer(
#            students,
#            many=True,
#            context={'request': request}
#        )
#        return serializer.data


class VacancyCreateSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    skills = PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    
    class Meta:
        fields = '__all__'
        model = Vacancy

    @transaction.atomic
    def create(self, validated_data):
        skills = validated_data.pop('skills')
        tags = validated_data.pop('tags')
        vacancy = Vacancy.objects.create(**validated_data)
        vacancy.skills.set(skills)
        vacancy.tags.set(tags)
        return vacancy

    @transaction.atomic
    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.skills.clear()
        instance.skills.set(skills)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return VacancySerializer(instance,
                                 context=context).data

    def validate_tags(self, value):
        if not value:
            raise ValidationError({
                'tags': 'Нужно выбрать хотя бы один тег'
            })
        if len(value) != len(set(value)):
            raise ValidationError({
                'tags': 'Теги не могут повторяться'
            })
        return value

    def validate_skills(self, value):
        if not value:
            raise ValidationError({
                'skills': 'Нужно выбрать хотя бы один навык'
            })
        if len(value) != len(set(value)):
            raise ValidationError({
                'skills': 'Навыки не могут повторяться'
            })
        return value


class VacancyCandidateSerializer(ModelSerializer):
    """Список кандидатов - откликнувшихся на вакансию и нет"""
    resp_candidates = SerializerMethodField()
    other_candidates = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            'resp_candidates',
            'other_candidates',
        )

    def get_resp_candidates(self, obj):
        return Resp.objects.filter(vacancy=obj)

    def get_other_candidates(self, obj):
        vacancy_name = obj.name
        # other_candidates = StudentUser.objects.filter(position__icontains=vacancy_name)
        #other_candidates = other_candidates.exclude(
        #    id__in=Resp.objects.filter(vacancy=obj).values('student_id')
        #)
        #return other_candidates
        
        return StudentUser.objects.all()

