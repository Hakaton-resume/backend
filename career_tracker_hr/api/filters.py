from django_filters.rest_framework import CharFilter, FilterSet
from django_filters.rest_framework.filters import (BooleanFilter,
                                                   ModelMultipleChoiceFilter)

from career.models import Vacancy, Tag
from users.models import Skill


class SkillFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Skill
        fields = ('name',)


class TagFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Tag
        fields = ('name',)
