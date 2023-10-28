import base64
from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ListField,
                                        ImageField, CharField,
                                        IntegerField)
from django.core.files.base import ContentFile
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.generics import get_object_or_404
from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.utils import percentage_of_similarity
from career.models import Favourite, Vacancy, Resp, Tag,  SkillVacancy, Invitation
from users.models import Company, StudentUser, Skill


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SkillSerializer(ModelSerializer):
    """Сериализатор для навыков"""
    class Meta:
        fields = ('name',)
        model = Skill


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов вакансии"""

    class Meta:
        fields = ('name',)
        model = Tag


class StudentSerializer(ModelSerializer):
    """Сериализатор для студентов"""
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = StudentUser
        fields = '__all__'


class StudenShortSerializer(ModelSerializer):
    """Сериализатор маленькой карточки студента"""
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = StudentUser
        fields = [
            'user',
            'photo',
            'location',
            'position',
            'experience',
            'skills'
        ]


class ResponseSerializer(ModelSerializer):
    """Сериализатор откликов"""
    student = StudenShortSerializer(read_only=True)
    similarity = SerializerMethodField()
    is_favourited = SerializerMethodField()
    is_invited = SerializerMethodField()
    
    class Meta:
        model = Resp
        fields = [
            'student',
            'similarity',
            'is_favourited',
            'is_invited',
        ]
        ordering = ['-similarity']


    def get_similarity(self, obj):
        vacancy_skills = obj.vacancy.skills.all()
        student_skills = obj.student.skills.all()
        return percentage_of_similarity(vacancy_skills, student_skills)

    def get_is_favourited(self, obj):
        return Favourite.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()

    def get_is_invited(self, obj):
        return Invitation.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()


class VacancyResponseSerializer(ModelSerializer):
    """Базовый сериализатор для вакансии"""
    tags = TagSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    response = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'name',
            'company',
            'tags',
            'skills',
            'response',
        ]


class CompanySerializer(ModelSerializer):
    vacancies = SerializerMethodField()

    class Meta:
        fields = ('name', 'vacancies')
        model = Company

    def get_vacancies(self, obj):
        vacancies = Vacancy.objects.filter(company=obj)
        serializer = VacancySerializer(vacancies, many=True)
        return serializer.data


class SkillWeightSerializer(ModelSerializer):
    name = CharField()
    weight = IntegerField(write_only=True)

    class Meta:
        fields = (
            'name',
            'weight',
        )
        model = SkillVacancy


class VacancySerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = (
            'name',
            'company',
            'tags',
            'skills',
        )


class VacancyCreateSerializer(ModelSerializer):
    """Сериализатор для создания вакансии"""
    tags = ListField(child=CharField())
    skills = SkillWeightSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Vacancy

    @transaction.atomic
    def weight_skills(self, skills, vacancy):
        for skill in skills:
            weight = skill['weight']
            skill = get_object_or_404(Skill, name=skill['name'])
            if Skill.objects.filter(name=skill).exists():
                skill = Skill.objects.get(name=skill)
            else:
                skill = Skill.objects.create(name=skill)
                vacancy.skills.add(skill)

        SkillVacancy.objects.create( 
                skill=skill,
                vacancy=vacancy,
                weight=weight
            )     

    @transaction.atomic
    def create(self, validated_data):
        skills = validated_data.pop('skills')
        tags = validated_data.pop('tags')
        vacancy = Vacancy.objects.create(**validated_data)
        self.weight_skills(skills, vacancy)

        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                tag = Tag.objects.get(name=tag)
            else:
                tag = Tag.objects.create(name=tag)
            vacancy.tags.add(tag)
        return vacancy

    @transaction.atomic
    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.skills.clear()
        self.weight_skills(skills, instance)
        instance.tags.clear()

        for tag in tags: 
            if Tag.objects.filter(name=tag).exists():
                tag = Tag.objects.get(name=tag) 
            else: 
                tag = Tag.objects.create(name=tag)
            instance.tags.add(tag)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return VacancySerializer(instance,
                                 context=context).data

    def validate_skills(self, value):
        if not value:
            raise ValidationError({
                'skill': 'Нужно ввести хотя бы один навык'
            })
        skills = []
        for item in value:
            skill = get_object_or_404(Skill, name=item['name'])
            if skill in skills:
                raise ValidationError({
                    'skill': 'Такой навык уже добавлен'
                })
            skills.append(skill)
        return value                             

    def validate_tags(self, value):
        if not value:
            raise ValidationError({
                'tag': 'Нужно выбрать хотя бы один тег'
            })
        if len(value) != len(set(value)):
            raise ValidationError({
                'tag': 'Теги не могут повторяться'
            })
        return value


class FavouriteCreateSerializer(ModelSerializer):
    student = StudenShortSerializer(read_only=True)

    class Meta:
        model = Resp
        fields = [
            'student',
        ]


class VacancyCreateFavouriteSerializer(ModelSerializer):
    favourite = FavouriteCreateSerializer(read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'name',
            'company',
            'tags',
            'skills',
            'favourite',
            ]
