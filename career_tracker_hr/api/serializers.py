import base64
from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ListField,
                                        ImageField, CharField,
                                        IntegerField, BooleanField)
from django.core.files.base import ContentFile
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.generics import get_object_or_404
from django.db import transaction
from rest_framework.exceptions import ValidationError

from api.utils import skills_compаration, experience_compаration, percentage_of_similarity
from career.models import Favourite, Vacancy, Resp, Tag,  SkillVacancy, Invitation
from users.models import Company, StudentUser, Skill, StudentsActivities, User


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
    activities = SerializerMethodField()
    last_name = SerializerMethodField()
    first_name = SerializerMethodField()
    photo = Base64ImageField()
    
    class Meta:
        model = StudentUser
        fields = '__all__'

    def get_activities(self, obj):
        activities = StudentsActivities.objects.filter(student=obj)
        return len(activities)

    def get_last_name(self, obj):
        user = get_object_or_404(User, email=obj.user)
        return user.last_name

    def get_first_name(self, obj):
        user = get_object_or_404(User, email=obj.user)
        return user.first_name


class StudentVacancySerializer(StudentSerializer):
    """Сериализатор для студентов в вакансии"""
    similarity = IntegerField()
    is_response = BooleanField()
    is_favourited = BooleanField()
    is_invitation = BooleanField()

    class Meta:
        model = StudentUser
        fields = '__all__'
        ordering = ['-similarity']


class VacancySerializer(ModelSerializer):
    "Базовый сериализатор для вакансии"
    tags = TagSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = '__all__'


class StudenShortSerializer(StudentSerializer):
    """Сериализатор короткой карточки студента"""

    class Meta:
        model = StudentUser
        fields = [
            'last_name',
            'first_name',
            'photo',
            'location',
            'position',
            'experience',
            'skills',
        ]


class BaseGroupSerializer(ModelSerializer):
    """Базовый сериализатор для разны групп студентов в вакансии"""
    student = StudentSerializer(read_only=True)
    similarity = SerializerMethodField()

    class Meta:
        model = Resp
        fields = '__all__'
        ordering = ['-similarity']

    def get_similarity(self, obj):
        vacancy_skills = obj.vacancy.skills.all()
        skills_with_weigth = []
        for skill in vacancy_skills:
            skill_weigth = SkillVacancy.objects.filter(
                vacancy=obj.vacancy, skill=skill
            ).first()
            weight = skill_weigth.weight
            skills_with_weigth.append((skill, weight))

        student_skills = obj.student.skills.all()
        skills_similarity = skills_compаration(
            skills_with_weigth, student_skills
        )
        vacancy_experience = obj.vacancy.experience
        student_experience = obj.student.experience
        experience_similarity = experience_compаration(
            vacancy_experience, student_experience
        )
        return percentage_of_similarity(
            skills_similarity, experience_similarity
        )


class ResponseSerializer(BaseGroupSerializer):
    """Сериализатор для откликов"""
    is_favourited = SerializerMethodField()
    is_invited = SerializerMethodField()

    def get_is_favourited(self, obj):
        return Favourite.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()

    def get_is_invited(self, obj):
        return Invitation.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()


class InvitationSerializer(BaseGroupSerializer):
    """Сериализатор для приглашений"""
    is_favourited = SerializerMethodField()
    is_response = SerializerMethodField()

    class Meta:
        model = Invitation
        fields = '__all__'
        ordering = ['-similarity']

    def get_is_favourited(self, obj):
        return Favourite.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()

    def get_is_response(self, obj):
        return Resp.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()


class FavouriteSerializer(BaseGroupSerializer):
    is_invitation = SerializerMethodField()
    is_response = SerializerMethodField()

    class Meta:
        model = Favourite
        fields = '__all__'

    def get_is_invitation(self, obj):
        return Invitation.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()

    def get_is_response(self, obj):
        return Resp.objects.filter(
            vacancy=obj.vacancy, student=obj.student
        ).exists()    


class VacancyResponseSerializer(VacancySerializer):
    """Cериализатор для вакансии c откликами"""
    response = ResponseSerializer(many=True, read_only=True)


class VacancyFavouriteSerializer(VacancySerializer):
    """Сериализатор для вакансий с избранным"""
    favourites = FavouriteSerializer(many=True, read_only=True)


class VacancyInvitationSerializer(VacancySerializer):
    """Сериализатор для вакансий с приглашениями"""
    invitations = InvitationSerializer(many=True, read_only=True)


class VacancyAllSerializer(VacancySerializer):
    """СЕриализатор для вакансии с откликами, избранными и приглашениями"""
    response = ResponseSerializer(many=True, read_only=True)
    favourites = FavouriteSerializer(many=True, read_only=True)
    invitations = InvitationSerializer(many=True, read_only=True)


class SkillWeightSerializer(ModelSerializer):
    """Сериализатор для навыков с весами в требованиях вакансии"""
    name = CharField()
    weight = IntegerField()

    class Meta:
        fields = (
            'name',
            'weight',
        )
        model = SkillVacancy


class VacancyCreateSerializer(ModelSerializer):
    """Сериализатор для создания вакансии"""
    tags = ListField(child=CharField())
    skills = SkillWeightSerializer(many=True)

    class Meta:
        fields = [
            "tags",
            "skills",
            "company_name",
            "company_info",
            "location",
            "pub_date",
            "name",
            "experience",
            "description",
            "responsibilities",
            "form",
            "reject_letter",
            "additional_info",
            "is_active",
            "salary",
            "currency"
        ]
        model = Vacancy

    @transaction.atomic
    def weight_skills(self, skills, vacancy):
        for skill_data in skills:
            weight = skill_data['weight']
            name = skill_data['name']
            if Skill.objects.filter(name=name).exists():
                skill = Skill.objects.filter(name=name).first()
            else:
                skill = Skill.objects.create(name=name)
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
        for tag_data in tags:
            if Tag.objects.filter(name=tag_data).exists():
                tag = Tag.objects.get(name=tag_data)
            else:
                tag = Tag.objects.create(name=tag_data)
            if not vacancy.tags.filter(name=tag_data).exists():
                vacancy.tags.add(tag)
        return vacancy

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'skills' in validated_data:
            skills = validated_data.pop('skills')
            instance.skills.clear()
            self.weight_skills(skills, instance)
        #skills = validated_data.pop('skills')
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.clear()
            for tag_data in tags: 
                if Tag.objects.filter(name=tag_data).exists():
                    tag = Tag.objects.get(name=tag_data) 
                else: 
                    tag = Tag.objects.create(name=tag_data)
                if not instance.tags.filter(name=tag_data).exists():
                    instance.tags.add(tag)
        instance = super().update(instance, validated_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return VacancySerializer(instance,
                                 context=context).data

    #def validate_skills(self, value):
    #    if not value:
    #        raise ValidationError({
    #            'skill': 'Нужно ввести хотя бы один навык'
    #        })
    #    skills = []
    #    for item in value:
    #        skill = get_object_or_404(Skill, name=item['name'])
    #        if skill in skills:
    #            raise ValidationError({
    #                'skill': 'Такой навык уже добавлен'
    #        })
    #        skills.append(skill)
    #    return value                             
   
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
