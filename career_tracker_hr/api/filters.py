from django_filters.rest_framework import CharFilter, FilterSet
from django_filters.rest_framework.filters import (BooleanFilter,
                                                   ModelMultipleChoiceFilter)

from career.models import Vacancy, Tag


class VacancyFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                     field_name='tags__name',
                                     to_field_name='name')
    is_favourited = BooleanFilter(
        field_name='is_favorited',
        method='is_something'
    )
    is_invited = BooleanFilter(
        field_name='is_invited',
        method='is_something'
    )

    class Meta:
        model = Vacancy
        fields = ('tags', 'is_favourite', 'is_invited',)

    def is_something(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if name == 'is_favorited' and value:
                return queryset.filter(favorites__user=user)
            if name == 'in_is_shopping_cart' and value:
                return queryset.filter(shopping_cart__user=user)
            return queryset
        return queryset