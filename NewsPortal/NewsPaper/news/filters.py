from django.forms import DateInput
from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post


class PostFilter(FilterSet):
    time_create = DateFilter(
        field_name='time_create',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
        label='Поиск по дате'
    )

    class Meta:
        model = Post
        fields = {
            'post_name': ['icontains'],
            'author': ['exact'],
        }
