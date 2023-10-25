from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.status import HTTP_400_BAD_REQUEST

from utils import percentage_of_similarity

# class SkillSerializer(ModelSerializer):
#
#    class Meta:
#        model = Skill
#        fields = '__all__'


#class RespSerializer(ModelSerializer):
#
#    class Meta:
#        model = Vacancy
#        fields = (
#            'id',
#            'name',
#        )
#
#    def validate(self, data):
#        user = self.context.get('request').user
#        vacancy = self.instance
#        if Resp.objects.filter(vacancy=vacancy, user=user).exists():
#            raise ValidationError(
#                detail='Вы уже откликались на эту вакансию',
#                code=HTTP_400_BAD_REQUEST
#            )
#        return data


#class VacancySerializer(ModelSerializer):
#    """Список кандидатов - откликнувшихся на вакансию и нет"""
#    resp_candidates = SerializerMethodField()
#    other_candidates = SerializerMethodField()
#
#    class Meta:
#        model = Vacancy
#        fields = (
#            'resp_candidates',
#            'other_candidates',
#        )
#
#    def get_resp_candidates(self, obj):
#        return Resp.objects.filter(vacancy=obj)
#
#    def get_other_candidates(self, obj):
#        vacancy_name = obj.name
#        other_candidates = Student.objects.filter(profession__icontains=vacancy_name)
#        other_candidates = other_candidates.exclude(
#            id__in=Resp.objects.filter(vacancy=obj).values('student_id')
        )
#        return other_candidates


#class VacancyCreateSerializer(ModelSerializer):
#    author = CustomUserSerializer(read_only=True)
#    skills = PrimaryKeyRelatedField(many=True, queryset=Skills.objects.all())
#    image = Base64ImageField()

#    class Meta:
#        fields = (
#            'id',
#            'skills',
#            'author',
#            'ingredients',
#            'is_favorited',
#            'is_in_shopping_cart',
#            'name',
#            'image',
#            'text',
#            'cooking_time'
#        )
#        model = Vacancy

#    @transaction.atomic
#    def create(self, validated_data):
#        skills = validated_data.pop('skills')
#        vacancy = Vacancy.objects.create(**validated_data)
#        vacancy.skills.set(skills)
#        return vacancy

#    @transaction.atomic
#    def update(self, instance, validated_data):
#        skills = validated_data.pop('skills')
#        instance = super().update(instance, validated_data)
#        instance.skills.clear()
#        instance.skills.set(skills)
#        instance.save()
#        return instance

#    def to_representation(self, instance):
#        request = self.context.get('request')
#        context = {'request': request}
#        return VacancySerializer(instance,
#                                context=context).data
#
#    def validate_skills(self, value):
#        if not value:
#            raise ValidationError({
#                'skills': 'Нужно выбрать хотя бы один навык'
#            })
#        if len(value) != len(set(value)):
#            raise ValidationError({
#                'skills': 'Навыки не могут повторяться'
#            })
#        return value

#class CandidateSerializer(ModelSerializer):
#        similarity = SerializerMethodField()
#        skills = SkillSerializer(many=True, read_only=True)
#
#    class Meta:
#        model = Student
#        fields = ('id',
#                  'name',
#                  'profession',
#                  'city',
#                  'experience',
#                  'skills',
#                  'similarity')
#        ordering = ['-similarity']
#
#    def get_similarity(self, obj):
#        vacancy = self.context['vacancy']
#        skills_vacancy = vacancy.skills
#        skills_student = obj.skills
#        return percentage_of_similarity(skills_vacancy, skills_student)
